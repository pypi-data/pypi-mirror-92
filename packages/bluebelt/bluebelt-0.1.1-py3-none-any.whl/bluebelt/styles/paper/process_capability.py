import bluebelt.helpers.defaults as defaults

# histogram | pyplot.hist
histogram = {
    'density': True, 
    'alpha': 1, # alpha fraction 0-1
    'edgecolor': None, # color name, hex or None
    'facecolor': defaults.blue, # color name, hex or None
    'fill': False, #True, False
    'hatch': '//', # '/', '\', '|', '-', '+', 'x', 'o', 'O', '.' or '*'
    'linestyle': 'solid', # '-', '--', '-.', ':', '', (offset, on-off-seq), ...
    'linewidth': 1, # float
}

histogram_patch_edge_color = defaults.red
histogram_patch_edge_hatch = '////'

# plot used for normal distribution | pyplot.plot
normal_plot = {
    'color': defaults.blue,
    'linestyle': 'dashed',
    'linewidth': 1,
}

# target axvline | pyplot.axvline
target_axvline = {
    'color': defaults.blue,
    'linestyle': 'dotted',
    'linewidth': 1,
}

# USL, LSL axvline | pyplot.axvline
sl_axvline = {
    'color': defaults.blue,
    'linestyle': 'dotted',
    'linewidth': 1,
}

# USL, LSL, target text | pyplot.text
sl_text = {
    'backgroundcolor': defaults.white,
    'va': 'center',
    'ha': 'center', 
}