from random import randint
from textwrap import dedent


def random_colour():
	return 'hsl(%d, 50%%, 85%%)' % randint(0, 359)


def display_list(items, grid=False, colour=True):
	grid_class = ' class="grid-list"' if grid else ''
	return dedent('''\
	<ul{}>
		{}
	</ul>
	'''.format(
		grid_class,
		'\n'.join('<li%s>%s</li>' %
			((' style="%s"' % item.get_style(colour)), item.display)
		for item in items)
	))