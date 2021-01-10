import datetime

import jwt
from django.http import HttpResponse
from django.shortcuts import render

import http.client


def zoom(request):
    import http.client

    conn = http.client.HTTPSConnection("api.zoom.us")

    headers = {
        'authorization': "Bearer eyJhbGciOiJIUzUxMiIsInYiOiIyLjAiLCJraWQiOiI5ZjJlZDZhMC0zZDQ4LTQyMmQtODRlOC1hOGMyYmMxNGRhNDkifQ.eyJ2ZXIiOjcsImF1aWQiOiIzYjg0NDNiZDc5ZjVmNjM5ZmI0MzViOGZkODBiNjFiMCIsImNvZGUiOiI1TUxUMno1eElvXzFyaFotZThyUzdpR2xnRjV1WFVreXciLCJpc3MiOiJ6bTpjaWQ6NkNlUWJFcnlSeWlDSFYyb3E4VU1TdyIsImdubyI6MCwidHlwZSI6MCwidGlkIjowLCJhdWQiOiJodHRwczovL29hdXRoLnpvb20udXMiLCJ1aWQiOiIxcmhaLWU4clM3aUdsZ0Y1dVhVa3l3IiwibmJmIjoxNjEwMTcyMTI3LCJleHAiOjE2MTAxNzU3MjcsImlhdCI6MTYxMDE3MjEyNywiYWlkIjoidzZ0OFdOOVRTRXlNSWJ0dFE0WDQwZyIsImp0aSI6ImMwMGRmNDA3LTk1MzgtNGEyYi1iNDdjLTg0OWJiMTAyY2FhZCJ9.MLu35Jg_tR0jNjXyaupLJZQpL5a7xDDnT1hvCNKOqn_EYkNSPux4k-znhYJjn4_0YbNaY9BSrgY3A8Q4ICT6rA"}

    conn.request("GET", "/v2/users?page_size=30&status=active", headers=headers)

    res = conn.getresponse()
    data = res.read()

    print(data.decode("utf-8"))

    return HttpResponse(data)
