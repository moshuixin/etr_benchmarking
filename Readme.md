# Install TTAA framework

First install TTAA framework using directory **requirement_packages** in this order:
  - ttaa_utils
  - ttaa_base

Type following command to install 
```sh
cd requirement_packages
pip install $package.zip --proxy $proxy_config
```

After finish installation, back to the main folder, for the first time run 
```sh
python manage.py migrate 
```
to set up database file

To run the development server type 
```sh
python manage.py runserver
```

In order to start server at different port
```sh
python manage.py runserver 127.0.0.1:9000
```# etr_benchmarking
