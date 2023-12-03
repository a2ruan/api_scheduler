title api_scheduler_frontend_server

pushd %~dp0
cd api_scheduler_frontend
npm run build
serve -s build -l 5555