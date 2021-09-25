import json

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from django.conf import settings

from events.models import Event

register=template.Library()


# Code to return checked if the amentity id is in the event
@register.simple_tag()
def is_checked(event_id, amentity_id):
	event = Event.objects.get(id=event_id)
	return 'checked' if event.amenities.filter(id=amentity_id).exists() else ''


# Code to return checked if the tool is included
@register.simple_tag()
def check_included_tool(value):
	return 'checked' if value.startswith('1') else ''


# Code to return checked if the tool is required
@register.simple_tag()
def check_required_tool(value):
	return 'checked' if value.endswith('1') else ''


# 


# Code to return html text for registered teams
@register.simple_tag()
def return_html(obj_list):

	html = ''

	# for i in settings.INFORMATION_TOOLS:
	# 	name = i['name']

	# 	if name != 'Line up':
	# 		value = obj.get(name, None)

	# 		if not value:
	# 			obj[name] = ''

	for i in settings.INFORMATION_TOOLS:
		key = i['name']

		key = 'line_up' if key == 'Line up' else key

		# Find if the key is available in the list
		found = False

		for obj in obj_list:
			value = obj.get(key, '')

			if value:
				found = True
				break
		
		if not found:
			if key == 'line_up':
				value = [{i: '', 'captain': ''} for i in ['First', 'Second', 'Third', 'Fourth']]
			else:
				value = ''

		# value = obj.get(key)

		if key == 'line_up':

			html += """<div class="registered-line-up">
						<h3>Line Up</h3>
						<hr>
			"""

			for team in value:

				for name, named in team.items():

					if name != 'captain':

						named = 'Not provided' if not named else named

						if team['captain'].lower() == 'yes':
							
							html += f"""
							<p class="mt-2 mb-0 d-flex align-items-center justify-content-between">
								<span><strong class="mr-3">{name}:</strong> {named}</span>
								<span class="badge badge-primary">Captain</span>
							</p>"""

						else:
							
							html += f"""<p class="mt-2 mb-0">
							<strong class="mr-3">{name}:
							</strong> {named}</p>"""

			html += "</div>"

		else:

			# print(key, value)

			value = 'Not provided' if not value else value

			html += f"""<p class="mt-2 mb-0 px-3">
			<strong class="mr-3">{key.capitalize()}:
			</strong> {value}</p>"""

	return mark_safe(html)



# for key, value in obj.items():

# 		if key == 'line_up':

# 			for team in value:

# 				for name, named in team.items():

# 					if name != 'captain':

# 						named = 'Not provided' if not named else named

# 						if team['captain'].lower() == 'yes':
							
# 							html += f"""
# 							<p class="mt-2 mb-0 d-flex align-items-center justify-content-between">
# 								<span><strong class="mr-3">{name}:</strong> {named}</span>
# 								<span class="badge badge-primary">Captain</span>
# 							</p>"""

# 						else:
							
# 							html += f"""<p class="mt-2 mb-0">
# 							<strong class="mr-3">{name}:
# 							</strong> {named}</p>"""

# 		else:

# 			print(key, value)

# 			value = 'Not provided' if not value else value

# 			html += f"""<p class="mt-2 mb-0">
# 			<strong class="mr-3">{key.capitalize()}:
# 			</strong> {value}</p>"""
