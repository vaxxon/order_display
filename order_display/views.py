from django.http import HttpResponse
from django.shortcuts import render
from order_display.api_test import get_info
import json

def main(request):
	return render(request, 'main.html')
	
def ajax(request):
	to_pick_data, delivery_data, return_data, run_data = get_info()
	args = {
		"to_pick_data": to_pick_data,
		"delivery_data": delivery_data,
		"return_data": return_data,
		"run_data": run_data,
	}
	args = json.dumps(args)
	return HttpResponse(args)