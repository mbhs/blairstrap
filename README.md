# Blairstrap

Blairstrap is the official Bootstrap skin for all modern Blair websites. It is
built and served from https://static.mbhs.edu.

## Planning

Blairstrap will be set up with GitHub hooks. When a branch commit is received,
the server will rebuild Bootstrap to reflect the changes and move them to 
the branches distribution location.

## GitHub Hooks Integration

The Blairstrap repository will come packaged with a custom Nginx config. Once
included, this config will determine a location where post requests are sent
by GitHub. When it receives these requests, it asynchronously rebuild the 
Blairstrap  repository and republish it to the static location.
