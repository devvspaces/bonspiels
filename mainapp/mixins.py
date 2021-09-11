from django.http import JsonResponse



def ajax_autocomplete(request, context):
	# Manage ajax request
    if request.is_ajax():
        tcd = request.GET.get('search-tcd')
        
        queryset = context['all_events']
        categories_set = context['all_categories']

        # Filter the querysets
        queryset = queryset.filter(title__icontains=tcd)
        categories_set = categories_set.filter(name__icontains=tcd)

        results = []

        for i in queryset:
            results.append(i.title)

        for i in categories_set:
            results.append(i.name)

        return JsonResponse(data={'results': results}, status=200)