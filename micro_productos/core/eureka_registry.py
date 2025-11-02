from py_eureka_client.eureka_client import EurekaClient

client = EurekaClient( eureka_server="http://localhost:8761/eureka", app_name="products-microservice", instance_port=8000, instance_host="localhost" )