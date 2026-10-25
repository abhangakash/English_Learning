import time
from django.db import connection
from django.test import Client
from django.test.utils import CaptureQueriesContext
from django.contrib.auth.models import User

t = time.time()
import speaking.pronunciation_engine
print("speaking.pronunciation_engine import:", round(time.time() - t, 2), "s")

t = time.time()
from django.urls import get_resolver
get_resolver().url_patterns
print("full URL config load:", round(time.time() - t, 2), "s")

def run(client, label, paths):
    for path in paths:
        for i in range(3):
            with CaptureQueriesContext(connection) as q:
                t = time.time()
                r = client.get(path, HTTP_HOST="localhost")
            print(f"{label} {path} run{i+1}: {r.status_code} {round((time.time()-t)*1000)} ms, {len(q)} queries")

anon = Client()
run(anon, "anon", ["/", "/login/"])

user = Client()
user.force_login(User.objects.get(username="Isha"))
run(user, "user", ["/profile/", "/speaking/start/", "/learning/level-selection/"])