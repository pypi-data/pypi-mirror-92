# process performance analysis
import copy

import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

import plotly.graph_objects as go

import bluebelt.analysis.ci as ci
import bluebelt.analysis.distribution as distribution

import bluebelt.helpers.defaults as defaults
import bluebelt.helpers.histogram
import bluebelt.helpers.mpl_format as mpl_format

import bluebelt.styles.paper as paper
#import bluebelt.styles.blue as blue


# process performance analysis
class Summary():
        
    def __init__(self, series, whis=1.5, **kwargs):
        
        self.series = series
        self.whis = whis
        self.calculate(whis)
        
    def __str__(self):
        str_mean="mean:"
        str_ci_mean="CI mean:"
        str_std="standard deviation:"
        str_min="minimum"
        str_q1="1st quantile:"
        str_median="median:"
        str_q3="3rd quantile:"
        str_max="maximum"
        str_ci_median="CI median:"
        str_ad_test="Anderson-Darling test"
        
        

        fill = 32
        return (f'{str_mean:{fill}}{self.mean:1.2f}\n' +
                f'{str_ci_mean:{fill}}{self.ci_mean[0]:1.2f}-{self.ci_mean[1]:1.2f}\n' +
                f'{str_std:{fill}}{self.std:1.2f}\n' +
                f'{str_min:{fill}}{self.min:1.2f}\n' +
                f'{str_q1:{fill}}{self.q1:1.2f}\n' +
                f'{str_median:{fill}}{self.median}\n' +
                f'{str_q3:{fill}}{self.q3:1.2f}\n' +
                f'{str_max:{fill}}{self.max:1.2f}\n' +
                f'{str_ci_median:{fill}}{self.ci_median[0]:1.2f}-{self.ci_median[1]:1.2f}\n' +
                f'{str_ad_test:{fill}}A={self.ad_test.statistic:1.2f}, p-value={self.ad_test.pvalue:1.2f}')
                

    def __repr__(self):
        return (f'{self.__class__.__name__}(mean={self.mean:1.1f}, std={self.std:1.1f}, min={self.min:1.1f}, q1={self.q1:1.1f}, median={self.median:1.1f}, q3={self.q3:1.1f}, max={self.max:1.1f})')
    
    def calculate(self, whis=1.5):
        
        self.mean = self.series.mean()
        self.ci_mean = ci.ci_mean(self.series)
        self.std = self.series.std()
        self.min = self.series.min()
        self.q1 = self.series.quantile(q=0.25)
        self.median = self.series.median()
        self.q3 = self.series.quantile(q=0.75)
        self.max = self.series.max()
        self.ci_median = ci.ci_median(self.series)
        self.ad_test = distribution.anderson_darling(self.series)
        self.boxplot_quantiles = self.get_boxplot_quantiles(whis=whis)
        self.boxplot_outliers = self.get_boxplot_outliers(whis=whis)
        
        
    def get_boxplot_quantiles(self, whis=1.5):
        # get the matplotlib boxplot quantiles
        # sort of direct copy from the matplotlib library

        q1, median, q3 = np.percentile(self.series, [25, 50, 75])

        if np.isscalar(whis):
            iqr = q3 - q1
            loval = q1 - (whis * iqr)
            hival = q3 + (whis * iqr)
        else:
            loval, hival = np.percentile(self.series, sorted(whis))

        # get high extreme
        wiskhi = self.series[self.series <= hival]
        if len(wiskhi) == 0 or np.max(wiskhi) < q3:
            high = q3
        else:
            high = np.max(wiskhi)

        # get low extreme
        wisklo = self.series[self.series >= loval]
        if len(wisklo) == 0 or np.min(wisklo) > q1:
            low = q1
        else:
            low = np.min(wisklo)
        
        return (low, q1, q3, high)

    def get_boxplot_outliers(self, whis=1.5):
        low, q1, q3, high = self.get_boxplot_quantiles(whis=whis)

        return self.series[self.series < low].append(self.series[self.series > high]).values
    
    def plot(self, **kwargs):

        style = kwargs.get('style', paper)
        kwargs.pop('style', None)
        path = kwargs.pop('path', None)

        # prepare figure
        fig = plt.figure(constrained_layout=False, **kwargs)
        gridspec = fig.add_gridspec(nrows=4, ncols=1, height_ratios=[8,3,3,3], wspace=0, hspace=0)
        ax1 = fig.add_subplot(gridspec[0, 0], zorder=50)
        ax2 = fig.add_subplot(gridspec[1, 0], zorder=40)
        ax3 = fig.add_subplot(gridspec[2, 0], zorder=30)
        ax4 = fig.add_subplot(gridspec[3, 0], zorder=20)

        # 1. histogram ############################################
        ax1.hist(self.series, **style.summary.histogram)

        # get current limits
        xlims = ax1.get_xlim()
        ylims = ax1.get_ylim()

        # fit a normal distribution to the data
        norm_mu, norm_std = stats.norm.fit(self.series)
        pdf_x = np.linspace(xlims[0], xlims[1], 100)
        ax1.plot(pdf_x, stats.norm.pdf(pdf_x, norm_mu, norm_std), **style.summary.normal_plot)

        # plot standard deviation
        if (self.mean-self.std) > self.min:
            std_area = np.linspace(self.mean-self.std, self.mean, 100)
            std_line_x = self.mean-self.std
            std_text_x = self.mean-self.std*0.5
        else:
            std_area = np.linspace(self.mean, self.mean+self.std, 100)
            std_line_x = self.mean+self.std
            std_text_x = self.mean+self.std*0.5

        ax1.fill_between(std_area, stats.norm.pdf(std_area, norm_mu, norm_std), 0, **style.summary.std_fill_between)
        
        ax1.axvline(x=self.mean, ymin=0, ymax=1, **style.summary.std_axvline)
        ax1.axvline(x=std_line_x, ymin=0, ymax=1, **style.summary.std_axvline)
        
        ax1.plot((std_line_x, self.mean), (ylims[1]*0.9, ylims[1]*0.9), **style.summary.std_axhline)
        ax1.text(std_text_x, ylims[1]*0.9, r'$\sigma = $'+f'{self.std:1.2f}', **style.summary.std_text)
        
        # plot AD test results
        if self.mean > (self.max + self.min) / 2:
            ad_x = 0.02
            ad_align = 'left'
        else:
            ad_x =  0.98
            ad_align = 'right'

        ad_result = distribution.anderson_darling(self.series)
        ad_text = r'$P_{AD, normal}: $'+f'{ad_result.pvalue:1.4f}'
        
        ax1.text(ad_x, 0.9, ad_text, transform=ax1.transAxes, va='center', ha=ad_align)

        # reset limits
        ax1.set_xlim(xlims)
        ax1.set_ylim(ylims)

        # 2. box plot ############################################
        boxplot = ax2.boxplot(self.series, vert=False, widths=0.3, whis=self.whis)
        
        for box in boxplot['boxes']:
            # add style if any is given
            box.set(**style.summary.boxplot.get('boxes', {}))

        ax2.set_xlim(xlims)
        ax2.set_ylim(0.7,1.7)

        ax2_xticks = self.boxplot_quantiles
        ax2.set_xticks(ax2_xticks)
        ax2.xaxis.set_major_formatter(FormatStrFormatter('%.1f'))
        

        

        #for tick in ax2.get_xticklabels():
        #    tick.set_horizontalalignment('left')

        #######################################################
        # CI for the median
        #######################################################

        ax3.plot([self.ci_median[0], self.ci_median[1]], [1,1], **style.summary.ci_mean_plot)
        ax3.axvline(x=self.ci_median[0], ymin=0.15, ymax=0.45, **style.summary.ci_mean_axvline)
        ax3.axvline(x=self.ci_median[1], ymin=0.15, ymax=0.45, **style.summary.ci_mean_axvline)
        ax3.scatter([self.median],[1], **style.summary.ci_mean_scatter)
        ax3.set_xlim(xlims)
        ax3_xticks = [self.ci_median[0], self.ci_median[1]]
        
        
        ax3.set_ylim(0.7,1.7)
        
        ci_median_x = 0.02 if self.median>(self.max+self.min)/2 else 0.98
        ci_median_align = 'left' if self.median>(self.max+self.min)/2 else 'right'
        
        ax3.text(ci_median_x, 0.1, r'$CI_{median}$', transform=ax3.transAxes, va='bottom', ha=ci_median_align)

        ax3.set_xticks(ax3_xticks)
        ax3.xaxis.set_major_formatter(FormatStrFormatter('%.1f'))


        #######################################################
        # CI for the mean
        #######################################################

        ax4.plot([self.ci_mean[0], self.ci_mean[1]], [1,1], **style.summary.ci_median_plot)
        ax4.axvline(x=self.ci_mean[0], ymin=0.15, ymax=0.45, **style.summary.ci_median_axvline)
        ax4.axvline(x=self.ci_mean[1], ymin=0.15, ymax=0.45, **style.summary.ci_median_axvline)
        ax4.scatter([self.mean],[1], **style.summary.ci_median_scatter)
        ax4.set_xlim(xlims)
        ax4_xticks = [self.ci_mean[0], self.ci_mean[1]]
        ax4.set_ylim(0.7,1.7)

        ci_mean_x = 0.02 if self.mean>(self.max+self.min)/2 else 0.98
        ci_mean_align = 'left' if self.mean>(self.max+self.min)/2 else 'right'
        
        ax4.text(ci_mean_x, 0.1, r'$CI_{mean}$', transform=ax4.transAxes, va='bottom', ha=ci_mean_align)

        # drop lines
        ax2.axvline(self.mean, ymin=0, ymax=2, **style.summary.drop_axvline)
        ax3.axvline(self.mean, ymin=0, ymax=1.7, **style.summary.drop_axvline)
        ax4.axvline(self.mean, ymin=0.3, ymax=1.7, **style.summary.drop_axvline)
        
        ax2.axvline(self.median, ymin=0, ymax=0.3, **style.summary.drop_axvline)
        ax3.axvline(self.median, ymin=0.3, ymax=1.7, **style.summary.drop_axvline)
        


        ax4.set_xticks(ax4_xticks)
        ax4.xaxis.set_major_formatter(FormatStrFormatter('%.1f'))
        

        ax1.set_title(f'graphical summary for {self.series.name}', **style.summary.title)

        ax1.set_yticks([])
        ax2.set_yticks([])
        ax3.set_yticks([])
        ax4.set_yticks([])

        if path:
            plt.savefig(path)
            plt.close()
        else:
            plt.close()
            return fig

class ControlChart():
    
    def __init__(self, series, **kwargs):
        
        self.series = series
        
        self.calculate()
        
    def __str__(self):
        str_mean="mean:"
        str_std="standard deviation:"
        str_ucl="upper control limit:"
        str_lcl=f"lower control limit:"
        str_outlier_count=f"outliers:"

        fill = 32
        return (f'{str_mean:{fill}}{self.mean:1.2f}\n' +
                f'{str_std:{fill}}{self.std:1.2f}\n' +
                f'{str_ucl:{fill}}{self.ucl:1.2f}\n' +
                f'{str_lcl:{fill}}{self.lcl:1.2f}\n' +
                f'{str_outlier_count:{fill}}{self.outlier_count}\n') 

    def __repr__(self):
        return (f'{self.__class__.__name__}(mean={self.mean:1.1f}, std={self.std:1.1f}, UCL={self.ucl:1.1f}, LCL={self.lcl:1.1f}, outlier_count={self.outlier_count:1.0f})')
    
    def calculate(self):
        mean = self.series.mean()
        std = self.series.std()
        ucl = mean + std * 3
        lcl = mean - std * 3
        outliers = self.series[(self.series > ucl) | (self.series < lcl)]
        
        self.mean = mean
        self.std = std
        self.ucl = ucl
        self.lcl = lcl
        self.outliers = outliers
        self.outlier_count = outliers.shape[0]
        
    def plot(self, **kwargs):
        
        style = kwargs.get('style', paper)
        kwargs.pop('style', None)

        path = kwargs.pop('path', None)
        
        fig, ax = plt.subplots(**kwargs)

        # observations
        ax.plot(self.series, **style.control_chart.plot)

        # observations white trail
        ax.plot(self.series, **style.control_chart.plot_background)

        # control limits
        ax.axhline(self.ucl, **style.control_chart.ucl_axhline)
        ax.axhline(self.lcl, **style.control_chart.lcl_axhline)

        ylim = ax.get_ylim() # get limits to set them back later
        xlim = ax.get_xlim()
        
        ax.fill_between(xlim, self.ucl, ylim[1], **style.control_chart.ucl_fill_between)
        ax.fill_between(xlim, self.lcl, ylim[0], **style.control_chart.lcl_fill_between)

        # outliers
        ax.plot(self.outliers, **style.control_chart.outlier_background)
        ax.plot(self.outliers, **style.control_chart.outlier)
        
        # mean
        ax.axhline(self.mean, **style.control_chart.mean_axhline)

        # text boxes for mean, UCL and LCL
        ax.text(xlim[1], self.mean, f' mean = {self.mean:1.2f}', **style.control_chart.mean_text)
        ax.text(xlim[1], self.ucl, f' UCL = {self.ucl:1.2f}', **style.control_chart.ucl_text)
        ax.text(xlim[1], self.lcl, f' LCL = {self.lcl:1.2f}', **style.control_chart.lcl_text)

        # reset limits
        ax.set_ylim(ylim)
        ax.set_xlim(xlim)

        # labels
        ax.set_title(f'control chart of {self.series.name}', **style.control_chart.title)
        #ax.set_xlabel(self.series.index.name)
        ax.set_ylabel('value')

        # set x axis locator
        mpl_format.axisformat(ax, self.series)

        plt.gcf().subplots_adjust(right=0.8)

        if path:
            plt.savefig(path)
            plt.close()
        else:
            plt.close()
            return fig
    
    def plotly(self, **kwargs):
        
        layout = go.Layout(
            title=f'control chart of {self.series.name}',    
            plot_bgcolor=f'rgba{defaults.white+(1,)}',
            hovermode="closest",
            xaxis=dict(
                title=self.series.index.name,
                linecolor=f'rgba{defaults.black+(1,)}',
                zeroline=False,
                ticks="outside",
                tickwidth=1,
                tickcolor=f'rgba{defaults.black+(1,)}',
                ticklen=5,
                showgrid=True,
                gridwidth=0.5,
                gridcolor=f'rgba{defaults.light_grey+(1,)}',
                mirror=True,
            ),
            yaxis=dict(
                title="value",
                linecolor=f'rgba{defaults.black+(1,)}',
                zeroline=False,
                ticks="outside",
                tickwidth=1,
                tickcolor=f'rgba{defaults.black+(1,)}',
                ticklen=5,
                showgrid=True,
                gridwidth=0.5,
                gridcolor=f'rgba{defaults.light_grey+(1,)}',
                mirror=True,
            ),
        )
        
        data = [go.Scatter(
                        x=self.outliers.index,
                        y=self.outliers.values,
                        marker=dict(
                            color=f'rgba{defaults.white+(1,)}',
                            line=dict(width=1, color=f'rgba{defaults.black+(1,)}'),
                            size=17,
                        ),
                        mode='markers',
                        showlegend=False,
                        name='outliers'
                    ),
                go.Scatter(
                        x=self.series.index,
                        y=self.series.values,
                        line=dict(
                                width=1,
                                color=f'rgba{defaults.blue+(1,)}',
                            ),
                        marker=dict(
                            color=f'rgba{defaults.black+(1,)}',
                            size=9,
                        ),
                        mode='lines+markers',
                        showlegend=False,
                        name=self.series.name,
                    ),
               ]
    
        fig = go.Figure(data=data, layout=layout)
    
    
        # add mean, UCL and LCL line
        fig.add_shape(
                type="line",
                xref="paper",
                yref="y",
                x0=0,
                y0=self.mean,
                x1=1,
                y1=self.mean,
                line=dict(
                    color=f'rgba{defaults.black+(1,)}',
                    width=1,
                    dash='dash'
                ),
            )
        fig.add_annotation(
            dict(
                xref="paper",
                yref="y",
                x=1,
                y=self.mean,
                text=f'mean = {self.mean:1.2f}',
                showarrow=False,
                align='right',
                bgcolor=f'rgba{defaults.white+(0.5,)}',
            )
        )
        fig.add_shape(
                type="line",
                xref="paper",
                yref="y",
                x0=0,
                y0=self.ucl,
                x1=1,
                y1=self.ucl,
                line=dict(
                    color=f'rgba{defaults.black+(1,)}',
                    width=0.5,
                    dash='dash'
                ),
            )
        fig.add_annotation(
            dict(
                xref="paper",
                yref="y",
                x=1,
                y=self.ucl,
                text=f'UCL = {self.ucl:1.2f}',
                showarrow=False,
                align='right',
                bgcolor=f'rgba{defaults.white+(0.5,)}',
            )
        )
        fig.add_shape(
                type="line",
                xref="paper",
                yref="y",
                x0=0,
                y0=self.lcl,
                x1=1,
                y1=self.lcl,
                line=dict(
                    color=f'rgba{defaults.black+(1,)}',
                    width=0.5,
                    dash='dash'
                ),
            )
        fig.add_annotation(
            dict(
                xref="paper",
                yref="y",
                x=1,
                y=self.lcl,
                text=f'LCL = {self.lcl:1.2f}',
                showarrow=False,
                align='right',
                bgcolor=f'rgba{defaults.white+(0.5,)}',
            )
        )
        # x-ticks to nice datetime format
        if isinstance(self.series.index, pd.DatetimeIndex):
            fig.update_layout(xaxis_tickformat = '%d-%m-%Y')
        
        # set width en height if any

        if 'width' in kwargs and 'height' in kwargs:
            fig.update_layout(width=kwargs.get('width'), height=kwargs.get('height'))

        return fig

class RunChart():
    def __init__(self,
                 series,
                 alpha=0.05
                ):
        
        self.series = series
        self.alpha = alpha
        
        self.calculate()
        
    def __str__(self):
        
        str_runs_about="runs about the median:"
        str_expected_runs_about="expected runs about the median:"
        str_longest_run_about="longest run about the median:"
        str_clustering=f"clustering (p ≈ {self.p_value_clustering:1.2f}):"
        str_mixtures=f"mixtures (p ≈ {self.p_value_mixtures:1.2f}):"
        
        str_runs_up_or_down="runs up or down:"
        str_expected_runs_up_or_down="expected runs up or down:"
        str_longest_run_up_or_down="longest run up or down:"
        str_trends=f"trends (p ≈ {self.p_value_trends:1.2f}):"
        str_oscillation=f"oscillation (p ≈ {self.p_value_oscillation:1.2f}):"

        fill = 32
        return (f'{str_runs_about:{fill}}{self.runs_about:1.0f}\n' +
                f'{str_expected_runs_about:{fill}}{self.expected_runs_about:1.0f}\n' +
                f'{str_longest_run_about:{fill}}{self.longest_run_about:1.0f}\n' +
                f'{str_clustering:{fill}}{self.clustering}\n' +
                f'{str_mixtures:{fill}}{self.mixtures}\n' +
                f'\n' +
                f'{str_runs_up_or_down:{fill}}{self.runs_up_or_down:1.0f}\n' +
                f'{str_expected_runs_up_or_down:{fill}}{self.expected_runs_up_or_down:1.0f}\n' +
                f'{str_longest_run_up_or_down:{fill}}{self.longest_run_up_or_down:1.0f}\n' +
                f'{str_trends:{fill}}{self.trends}\n' +
                f'{str_oscillation:{fill}}{self.oscillation}')


    def __repr__(self):
        return (f'{self.__class__.__name__}(runs_about={self.runs_about:1.0f}, expected_runs_about={self.expected_runs_about:1.0f}, longest_run_about={self.longest_run_about:1.0f}, runs_up_or_down={self.runs_up_or_down:1.0f}, expected_runs_up_or_down={self.expected_runs_up_or_down:1.0f}, longest_run_up_or_down={self.longest_run_up_or_down:1.0f}, p_value_clustering={self.p_value_clustering:1.2f}, p_value_mixtures={self.p_value_mixtures:1.2f}, p_value_trends={self.p_value_trends:1.2f}, p_value_oscillation={self.p_value_oscillation:1.2f}, clustering={self.clustering}, mixtures={self.mixtures}, trends={self.trends}, oscillation={self.oscillation})')

    def metrics(self):
        str_runs_about="runs about the median:"
        str_expected_runs_about="expected runs about the median:"
        str_longest_run_about="longest run about the median:"
        str_clustering=f"clustering (p ≈ {self.p_value_clustering:1.2f}):"
        str_mixtures=f"mixtures (p ≈ {self.p_value_mixtures:1.2f}):"
        
        str_runs_up_or_down="runs up or down:"
        str_expected_runs_up_or_down="expected runs up or down:"
        str_longest_run_up_or_down="longest run up or down:"
        str_trends=f"trends (p ≈ {self.p_value_trends:1.2f}):"
        str_oscillation=f"oscillation (p ≈ {self.p_value_oscillation:1.2f}):"

        fill = 32
        print( (f'{str_runs_about:{fill}}{self.runs_about:1.0f}\n' +
                f'{str_expected_runs_about:{fill}}{self.expected_runs_about:1.0f}\n' +
                f'{str_longest_run_about:{fill}}{self.longest_run_about:1.0f}\n' +
                f'{str_clustering:{fill}}{self.clustering}\n' +
                f'{str_mixtures:{fill}}{self.mixtures}\n' +
                f'\n' +
                f'{str_runs_up_or_down:{fill}}{self.runs_up_or_down:1.0f}\n' +
                f'{str_expected_runs_up_or_down:{fill}}{self.expected_runs_up_or_down:1.0f}\n' +
                f'{str_longest_run_up_or_down:{fill}}{self.longest_run_up_or_down:1.0f}\n' +
                f'{str_trends:{fill}}{self.trends}\n' +
                f'{str_oscillation:{fill}}{self.oscillation}'))
    
    def calculate(self):
        '''
        The number of runs about the median is the total number of runs above the median and 
        the total number of runs below the median.
        A run about the median is one or more consecutive points on the same side of the center line.
        A run ends when the line that connects the points crosses the center line.
        A new run begins with the next plotted point. 
        A data point equal to the median belongs to the run below the median.

        The number of runs up or down is the total count of upward and downward runs in the series.
        A run up or down ends when the direction changes.


        Clustering, mixtures, trends and oscillation
        A p-value that is less than the specified level of significance indicates clustering, mixtures, trends and/or oscillation
        '''

        median = self.series.median()

        longest_runs_about = [] #pd.Series(dtype=object)[
        longest_runs_up_or_down = [] #pd.Series(dtype=object)

        # runs

        for index, value in self.series.iteritems():

            # runs about the median
            if index == self.series.index[0]: # set above and start the first run
                above = True if value > median else False
                longest_run_about = 1
                run_about_length = 1
                runs_about = 0
            elif (value > median and not above) or (value <= median and above): # new run about
                runs_about += 1 # add an extra run
                above = not above # toggle the above value
                if run_about_length > longest_run_about:
                    longest_run_about = run_about_length
                    longest_runs_about = [self.series.loc[:index].iloc[-(longest_run_about+1):-1]]
                elif run_about_length == longest_run_about:
                    longest_runs_about += [self.series.loc[:index].iloc[-(longest_run_about+1):-1]]
                #longest_run_about = max(longest_run_about, run_about_length)
                run_about_length = 1
            elif index == self.series.index[-1]: # the last value might bring a longest run
                run_about_length += 1
                if run_about_length > longest_run_about:
                    longest_run_about = run_about_length
                    longest_runs_about = [self.series.loc[:index].iloc[-(longest_run_about):]]
                elif run_about_length == longest_run_about:
                    longest_runs_about += [self.series.loc[:index].iloc[-(longest_run_about):]]
            else:
                run_about_length += 1

            # runs up or down
            if index == self.series.index[0]: # set the first value
                previous_value = value
            elif index == self.series.index[1]: # set up and start first run
                up = True if value > previous_value else False
                longest_run_up_or_down = 1
                run_up_or_down_length = 1
                runs_up_or_down = 1
                previous_value = value

            elif (value > previous_value and not up) or (value <= previous_value and up): # new run up or down
                runs_up_or_down += 1 # add an extra run
                up = not up # toggle up
                if run_up_or_down_length > longest_run_up_or_down:
                    longest_run_up_or_down = run_up_or_down_length
                    longest_runs_up_or_down = [self.series.loc[:index][-(longest_run_up_or_down+1):-1]]
                elif run_up_or_down_length == longest_run_up_or_down:
                    longest_runs_up_or_down += [self.series.loc[:index][-(longest_run_up_or_down+1):-1]]   
                run_up_or_down_length = 1
                previous_value = value

            elif index == self.series.index[-1]: # the last value might bring a longest run
                run_up_or_down_length += 1
                if run_up_or_down_length > longest_run_up_or_down:
                    longest_run_up_or_down = run_up_or_down_length
                    longest_runs_up_or_down = [self.series.loc[:index].iloc[-(longest_run_up_or_down):]]
                elif run_up_or_down_length == longest_run_up_or_down:
                    longest_runs_up_or_down += [self.series.loc[:index].iloc[-(longest_run_up_or_down):]]

            else:
                run_up_or_down_length += 1
                previous_value = value



        # expected runs
        m = self.series[self.series > self.series.median()].count()
        n = self.series[self.series <= self.series.median()].count()
        N = self.series.count()

        expected_runs_about = 1 + (2 * m * n) / N

        expected_runs_up_or_down = (2 * (m + n) - 1) / 3

        # clustering and mixtures
        p_value_clustering = stats.norm.cdf((runs_about - 1 - ((2 * m * n) / N)) / (((2 * m * n * (2 * m * n - N)) / (N**2 * (N - 1)))**0.5))
        p_value_mixtures = 1 - p_value_clustering

        clustering = True if p_value_clustering < self.alpha else False
        mixtures = True if p_value_mixtures < self.alpha else False

        # trends and oscillation
        p_value_trends = stats.norm.cdf((runs_up_or_down - (2 * N - 1) / 3) / ((16 * N - 29) / 90)**0.5)
        p_value_oscillation = 1 - p_value_trends

        trends = True if p_value_trends < self.alpha else False
        oscillation = True if p_value_oscillation < self.alpha else False
        
        self.runs_about = runs_about
        self.expected_runs_about = expected_runs_about
        self.longest_run_about = longest_run_about
        self.runs_up_or_down = runs_up_or_down
        self.expected_runs_up_or_down = expected_runs_up_or_down
        self.longest_run_up_or_down = longest_run_up_or_down
        self.p_value_clustering = p_value_clustering
        self.p_value_mixtures = p_value_mixtures
        self.p_value_trends = p_value_trends
        self.p_value_oscillation = p_value_oscillation
        self.clustering = clustering
        self.mixtures = mixtures
        self.trends = trends
        self.oscillation = oscillation
        self.longest_runs_about = longest_runs_about
        self.longest_runs_up_or_down = longest_runs_up_or_down
        
    def plot(self, **kwargs):
        
        style = kwargs.get('style', paper)
        kwargs.pop('style', None)

        path = kwargs.pop('path', None)        
        
        fig, ax = plt.subplots(nrows=1, ncols=1, **kwargs)
        
        # observations
        ax.plot(self.series, **style.run_chart.plot)
        

        # longest run(s) about the median and longest run(s) up or down
        ylim = ax.get_ylim() # get ylim to set it back later

        for run in self.longest_runs_about:
            ax.fill_between(run.index, run.values, ylim[0], **style.run_chart.longest_runs_about_fill_between)

        for run in self.longest_runs_up_or_down:
            ax.fill_between(run.index, run.values, ylim[1], **style.run_chart.longest_runs_up_or_down_fill_between)
        
        ax.set_ylim(ylim[0], ylim[1]) # reset ylim

        # mean
        ax.axhline(self.series.median(), zorder=1, **style.run_chart.median_axhline)
        ax.text(ax.get_xlim()[1], self.series.median(), f' median = {self.series.median():1.2f}', **style.run_chart.median_text)

        ax.text(ax.get_xlim()[1], ylim[0], f' longest {"run" if len(self.longest_runs_about)==1 else "runs"}\n about the\n median = {self.longest_run_about}', **style.run_chart.longest_runs_about_text)
        ax.text(ax.get_xlim()[1], ylim[1], f' longest {"run" if len(self.longest_runs_up_or_down)==1 else "runs"}\n up or down = {self.longest_run_up_or_down}', **style.run_chart.longest_runs_up_or_down_text)

        # labels
        ax.set_title(f'run chart of {self.series.name}', **style.run_chart.title)
        #ax.set_xlabel(self.series.index.name)
        ax.set_ylabel('value')

        # set x axis locator
        mpl_format.axisformat(ax, self.series)

        plt.gcf().subplots_adjust(right=0.8)

        if path:
            plt.savefig(path)
            plt.close()
        else:
            plt.close()
            return fig

        
    def plotly(self, **kwargs):
        
        layout = go.Layout(
            title=f'run chart of {self.series.name}',    
            plot_bgcolor=f'rgba{defaults.white+(1,)}',
            hovermode="closest",
            xaxis=dict(
                title=self.series.index.name,
                linecolor=f'rgba{defaults.black+(1,)}',
                zeroline=False,
                ticks="outside",
                tickwidth=1,
                tickcolor=f'rgba{defaults.black+(1,)}',
                ticklen=5,
                showgrid=True,
                gridwidth=0.5,
                gridcolor=f'rgba{defaults.light_grey+(0.2,)}',
                mirror=True,
            ),
            yaxis=dict(
                title="value",
                linecolor=f'rgba{defaults.black+(1,)}',
                zeroline=False,
                ticks="outside",
                tickwidth=1,
                tickcolor=f'rgba{defaults.black+(1,)}',
                ticklen=5,
                showgrid=True,
                gridwidth=0.5,
                gridcolor=f'rgba{defaults.light_grey+(1,)}',
                mirror=True,
            ),
        )
        
        data = []
        
        for idx, trace in enumerate(self.longest_runs_about):
            data.append(go.Scatter(
                x=trace.index,
                y=trace.values,
                line=dict(
                    width=9,
                    color=f'rgba{defaults.red+(0.4,)}',
                ),
                mode='lines',
                name=f'longest {"run" if len(self.longest_runs_about)==1 else "runs"} about the median ({self.longest_run_about})',
                legendgroup="runs_about",
                showlegend=True if idx==0 else False,
            ))

        for idx, trace in enumerate(self.longest_runs_up_or_down):
            data.append(go.Scatter(
                x=trace.index,
                y=trace.values,
                line=dict(
                    width=9,
                    color=f'rgba{defaults.blue+(0.4,)}',
                ),
                mode='lines',
                name=f'longest {"run" if len(self.longest_runs_up_or_down)==1 else "runs"} up or down ({self.longest_run_up_or_down})',
                legendgroup="runs_up_down",
                showlegend=True if idx==0 else False,
            ))


        data.append(go.Scatter(
            x=self.series.index,
            y=self.series.values,
            line=dict(
                    width=1,
                    color=f'rgba{defaults.blue+(1,)}',
                ),
            marker=dict(
                color=f'rgba{defaults.black+(1,)}',
                size=5,
            ),
            mode='lines+markers',
            showlegend=False,
        ))
        
        fig = go.Figure(data=data, layout=layout)

        # legend position
        fig.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ))

    
        # add median line
        fig.add_shape(
                type="line",
                xref="paper",
                yref="y",
                x0=0,
                y0=self.series.median(),
                x1=1,
                y1=self.series.median(),
                line=dict(
                    color=f'rgba{defaults.grey+(1,)}',
                    width=1,
                    dash='dash'
                ),
            )
        fig.add_annotation(
            dict(
                xref="paper",
                yref="y",
                x=1,
                y=self.series.median(),
                text=f'median = {self.series.median():1.2f}',
                showarrow=False,
                align='right',
                bgcolor=f'rgba{defaults.white+(0.5,)}',
            )
        )
        
        # x-ticks to nice datetime format
        if isinstance(self.series.index, pd.DatetimeIndex):
            fig.update_layout(xaxis_tickformat = '%d-%m-%Y')
        
        # set width en height if any
        if 'width' in kwargs and 'height' in kwargs:
            fig.update_layout(width=kwargs.get('width'), height=kwargs.get('height'))

        return fig

class ProcessCapability():
    def __init__(self,
                 series,
                 target=None,
                 usl=None,
                 ub=False,
                 lsl=None,
                 lb=False,
                ):
        
        self.series = series
        self.min = series.values.min()
        self.max = series.values.max()
        self.target = target
        self.usl = usl
        self.lsl = lsl
        self.ub = ub
        self.lb = lb
        self.sample_size = len(series)
        
        self.calculate()
        
    def __str__(self):
        str_target="target"
        str_lsl="LB" if self.lb else "LSL" 
        str_usl="UB" if self.ub else "USL"
        str_lt_lsl="% < LSL"
        str_gt_usl="% > USL"
        str_observed_performance="Observed Performance"
        str_pp="Pp"
        str_ppk="Ppk"
        
        

        fill = 32
        return (f'{str_target:{fill}}{self.target}\n' +
                f'{str_lsl:{fill}}{self.lsl}\n' +
                f'{str_usl:{fill}}{self.usl}\n' +
                f'{str_lt_lsl:{fill}}{self.lt_lsl:1.4f}\n' +
                f'{str_gt_usl:{fill}}{self.gt_usl:1.4f}\n' +
                f'{str_observed_performance:{fill}}{self.observed_performance:1.4f}\n' +
                f'{str_pp:{fill}}{self.pp:1.4f}\n' +
                f'{str_ppk:{fill}}{self.ppk:1.4f}')

    def __repr__(self):
        lsl_text = 'lb' if self.lb else 'lsl'
        usl_text = 'ub' if self.ub else 'usl'

        return (f'{self.__class__.__name__}(n={self.sample_size}, target={self.target}, {lsl_text}={self.lsl}, {usl_text}={self.usl}, observed={self.observed_performance:1.4f})')
    
    def df(self):
        df_md = pd.DataFrame({
            'metric': ["target", "LB" if self.lb else "LSL", "UB" if self.ub else "USL", "% < LSL", "% > USL", "Observed Performance", "Pp", "Ppk"],
            'value': [self.target, self.lsl, self.usl, self.lt_lsl, self.gt_usl, self.observed_performance, self.pp, self.ppk],
            }
        )
        
        return df_md

    def md(self):
        print(self.df().to_markdown(index=False))

    def calculate(self):
        mean = self.series.mean()
        std = self.series.std()
        
        # lsl and usl to calculate performance
        self._plsl = self.lsl or self.min
        self._pusl = self.usl or self.max

        self.mean = mean
        self.std = std
        self.lt_lsl = (self.series[self.series < self._plsl].count() / self.sample_size)
        self.gt_usl = (self.series[self.series > self._pusl].count() / self.sample_size)
        self.observed_performance = self.series[(self.series >= self._plsl) & (self.series <= self._pusl)].count() / self.sample_size
        self.pp = (self._pusl - self._plsl) / (6 * self.std) # Pp = (USL – LSL) / 6 * sigma
        self.ppk = (min(self.mean - self._plsl, self._pusl - self.mean)) / (3 * self.std) # Ppk = [ min(USL – x(bar), x(bar) - LSL) ] / 3 s

        
    def plot(self, **kwargs):
        
        style = kwargs.get('style', paper)
        kwargs.pop('style', None)

        path = kwargs.pop('path', None)

        # get bins
        min_bins = kwargs.pop('min_bins', 10)
        max_bins = kwargs.pop('max_bins', 20)

        histogram_points = [x for x in [self.lsl, self.usl, self.target] if x is not None]
        bins = bluebelt.helpers.histogram.bins(series=self.series, points=histogram_points, min_bins=min_bins, max_bins=max_bins)

        def _set_patch_style(patch, style):
            for key in ['facecolor', 'edgecolor', 'linewidth', 'hatch', 'fill']:
                if key in style:
                    eval(f'patch.set_{key}(style.get(key))')
        
        fig, ax = plt.subplots(nrows=1, ncols=1, **kwargs)
        
        # 1. histogram ############################################
        n, bins, patches = ax.hist(self.series, bins=bins, **style.process_capability.histogram)

        for patch in patches:
            # catch patches 

            # LSL
            if self.lsl is not None:

                # < LSL
                if patch.get_x() + patch.get_width() <= self.lsl:
                    patch.set_fill(False)
                    patch.set_hatch('')
                    patch_copy = copy.copy(patch)
                    _set_patch_style(patch_copy, style.process_capability.histogram_fill_out_of_range)
                    ax.add_patch(patch_copy)

                # on LSL
                elif patch.get_x() < self.lsl and patch.get_x() + patch.get_width() > self.lsl:
                    # split patch
                    patch.set_fill(False)
                    patch.set_hatch('')
                    # first half
                    patch_width_1 = self.lsl - patch.get_x()
                    patch_copy = copy.copy(patch)
                    _set_patch_style(patch_copy, style.process_capability.histogram_fill_out_of_range)
                    patch_copy.set_width(patch_width_1)
                    ax.add_patch(patch_copy)
                
                    # second half
                    patch_width_2 = (patch.get_x()+patch.get_width()) - self.lsl
                    patch_copy = copy.copy(patch)
                    _set_patch_style(patch_copy, style.process_capability.histogram_fill_in_range)
                    patch_copy.set_width(patch_width_2)
                    patch_copy.set_x(patch.get_x()+patch_width_1)
                    ax.add_patch(patch_copy)
            
            if self.usl is not None:
                # > USL
                if patch.get_x() >= self.usl:
                    patch.set_fill(False)
                    patch.set_hatch('')
                    patch_copy = copy.copy(patch)
                    _set_patch_style(patch_copy, style.process_capability.histogram_fill_out_of_range)
                    ax.add_patch(patch_copy)

                # on USL
                elif patch.get_x() <= self.usl and patch.get_x() + patch.get_width() > self.usl:
                    # split patch
                    patch.set_fill(False)
                    patch.set_hatch('')
                    # first half
                    patch_width_1 = self.usl - patch.get_x()
                    patch_copy = copy.copy(patch)
                    _set_patch_style(patch_copy, style.process_capability.histogram_fill_in_range)
                    patch_copy.set_width(patch_width_1)
                    ax.add_patch(patch_copy)
                    
                    # second half
                    patch_width_2 = (patch.get_x()+patch.get_width()) - self.usl
                    patch_copy = copy.copy(patch)
                    _set_patch_style(patch_copy, style.process_capability.histogram_fill_out_of_range)
                    patch_copy.set_width(patch_width_2)
                    patch_copy.set_x(patch.get_x()+patch_width_1)
                    ax.add_patch(patch_copy)

        # get current limits
        xlims = ax.get_xlim()
        ylims = ax.get_ylim()

        # fit a normal distribution to the data
        norm_mu, norm_std = stats.norm.fit(self.series)
        pdf_x = np.linspace(xlims[0], xlims[1], 100)
        ax.plot(pdf_x, stats.norm.pdf(pdf_x, norm_mu, norm_std), **style.process_capability.normal_plot)
        
        # target
        if self.target:
            ax.axvline(x=self.target, ymin=0, ymax=1, **style.process_capability.target_axvline)
            ax.text(self.target, ylims[1]*0.9, f'target', **style.process_capability.sl_text)

        # LSL, USL
        if self.lsl:
            ax.axvline(x=self.lsl, ymin=0, ymax=1, **style.process_capability.sl_axvline)
            lsl_text = 'LB' if self.lb else 'LSL'
            ax.text(self.lsl, ylims[1]*0.9, lsl_text, **style.process_capability.sl_text)
        
        if self.usl:
            ax.axvline(x=self.usl, ymin=0, ymax=1, **style.process_capability.sl_axvline)
            usl_text = 'UB' if self.ub else 'USL'
            ax.text(self.usl, ylims[1]*0.9, usl_text, **style.process_capability.sl_text)

        # change xlim if needed
        xlims_min = min(self.series.values.min(), self._plsl, self._pusl, self.target)
        xlims_max = max(self.series.values.max(), self._plsl, self._pusl, self.target)
        xlims_margin = (xlims_max - xlims_min) * plt.rcParams['axes.xmargin']
        xlims = (xlims_min - xlims_margin, xlims_max + xlims_margin)
        
        # reset limits
        ax.set_xlim(xlims)
        ax.set_ylim(ylims)

        plt.gcf().subplots_adjust(right=0.8)

        if path:
            plt.savefig(path)
            plt.close()
        else:
            plt.close()
            return fig
