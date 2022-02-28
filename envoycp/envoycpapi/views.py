from django.shortcuts import render
from django.http import HttpResponse
import json
import redis
import subprocess
from os.path import exists
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def endpoint_discovery(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    content = body
    try:
      r = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)
    except Exception as e:
      print("Can not connect to redis : %s",e)
    try:
      existing_version_of_endpoints = body["version_info"]
    except Exception:
      existing_version_of_endpoints = 0
    try:
      if r.get("endpoints_conf_version_info") is not None:
        endpoints_version = r.get("endpoints_conf_version_info")
      else:
        endpoints_version = 0
    except Exception:
      endpoints_version = 0

    #print(content)
    
    resp =  {
                  "version_info": str(endpoints_version),
                  "resources": [ 
                      {
                        "@type":"type.googleapis.com/envoy.config.endpoint.v3.ClusterLoadAssignment",
                        "cluster_name": "myservice",
                        "endpoints": [
                            {
                                "lb_endpoints": {"endpoint": {
                                                    "address":  {
                                                       "socket_address": {
                                                           "address": "127.0.0.1",
                                                           "port_value":  1234
                                                       }
                                                    }
                                                }}
                            }
                        ]
                      }
                  ]
            }
    response = HttpResponse(json.dumps(resp))
    if int(endpoints_version) > int(existing_version_of_endpoints):
      response.status_code = 200
    else:
      response.status_code = 304
    return response

@csrf_exempt
def cluster_discovery(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    content = body
    try:
      r = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)
    except Exception as e:
      print("Can not connect to redis : %s",e)
    try:
      existing_version_of_clusters = body["version_info"]
    except Exception:
      existing_version_of_clusters = 0
    try:
      if r.get("clusters_conf_version_info") is not None:
        clusters_version = r.get("clusters_conf_version_info")
      else:
        clusters_version = 0
    except Exception:
      clusters_version = 0
    resp = {
                  "version_info": str(clusters_version),
                  "resources": [ 
                      {
                        "@type":"type.googleapis.com/envoy.config.cluster.v3.Cluster",
                        "name": "test_clusterr",
                        "endpoints": [
                            {
                                "lb_endpoints": {"endpoint": {
                                                    "address":  {
                                                       "socket_address": {
                                                           "address": "127.0.0.1",
                                                           "port_value":  7777
                                                       }
                                                    }
                                                }}
                            }
                        ]
                      },
                      {
                        "@type":"type.googleapis.com/envoy.config.cluster.v3.Cluster",
                        "name": "targetCluster",
                        "endpoints": [
                            {
                                "lb_endpoints": {"endpoint": {
                                                    "address":  {
                                                       "socket_address": {
                                                           "address": "127.0.0.1",
                                                           "port_value":  8888
                                                       }
                                                    }
                                                }}
                            }
                        ]
                      },
                      {
                        "@type":"type.googleapis.com/envoy.config.cluster.v3.Cluster",
                        "name": "edscluster",
                        "endpoints": [
                            {
                                "lb_endpoints": {"endpoint": {
                                                    "address":  {
                                                       "socket_address": {
                                                           "address": "127.0.0.1",
                                                           "port_value":  9999
                                                       }
                                                    }
                                                }}
                            }
                        ]
                      }
                  ]
            }
    response = HttpResponse(json.dumps(resp))
    if(int(clusters_version) > int(existing_version_of_clusters)):
      response.status_code = 200
    else:
      response.status_code = 304
    return response


@csrf_exempt
def listener_discovery(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    content = body
    try:
      r = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)
    except Exception as e:
      print("Can not connect to redis : %s",e)
    try:
      existing_version_of_listeners = body["version_info"]
    except Exception:
      existing_version_of_listeners = 0
    try:
      if r.get("listeners_conf_version_info") is not None:
        listeners_version = r.get("listeners_conf_version_info")
      else:
        listeners_version = 0
    except Exception:
      listeners_version = 0
    resp = {
                  "version_info": str(listeners_version),
                  "resources": [ 
                      {
                        "@type":"type.googleapis.com/envoy.config.listener.v3.Listener",
                        "name": "listener_x_1",
                        "address": 
                            {                                
                                "socket_address": {
                                    "address": "127.0.0.1",
                                    "port_value":  4445
                                }
                            },
                        "filter_chains": [
                          {
                            "filters": [
                              {
                                "name": "envoy.filters.network.http_connection_manager",
                                "typed_config": {
                                  "@type": "type.googleapis.com/envoy.extensions.filters.network.http_connection_manager.v3.HttpConnectionManager",
                                  "stat_prefix": "edge",
                                  "http_filters": [
                                    {
                                      "name": "envoy.filters.http.router"
                                    }
                                  ],
                                  "route_config": {
                                    "virtual_hosts": [
                                      {
                                        "name": "all_domains",
                                        "domains": [
                                          "*"
                                        ]
                                      }
                                    ]
                                  }
                                }
                              }
                            ]
                          }
                        ]                        
                      }
                  ]
            }
    response = HttpResponse(json.dumps(resp))
    if(int(listeners_version) > int(existing_version_of_listeners)):
      response.status_code = 200
    else:
      response.status_code = 304
    return response

@csrf_exempt
def increment_eds_version(request):
  try:
    r = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)
  except Exception as e:
    print("Can not connect to redis : %s",e)
  try:
    r.incr("endpoints_conf_version_info")
    return HttpResponse("eds version increment successfully.")
  except Exception as e:
    r.set("endpoints_conf_version_info","1")
    print("Error : %s",e)
    return HttpResponse("eds version increment failed. Set to 1")

@csrf_exempt
def increment_cds_version(request):
  try:
    r = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)
  except Exception as e:
    print("Can not connect to redis : %s",e)
  try:
    r.incr("clusters_conf_version_info")
    return HttpResponse("cds version increment successfully.")
  except Exception as e:
    r.set("endpoints_conf_version_info","1")
    print("Error : %s",e)
    return HttpResponse("cds version increment failed. Set to 1")

@csrf_exempt
def increment_lds_version(request):
  try:
    r = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)
  except Exception as e:
    print("Can not connect to redis : %s",e)
  try:
    r.incr("listeners_conf_version_info")
    return HttpResponse("lds version increment successfully.")
  except Exception as e:
    r.set("endpoints_conf_version_info","1")
    print("Error : %s",e)
    return HttpResponse("lds version increment failed. Set to 1")

@csrf_exempt
def start_envoy(request):
  
  print("envoy is starting...")
  file_exists = exists("/usr/local/bin/func-e")
  if file_exists:
    print("func-e is available")
    #TODO 
    subprocess.run(["func-e run -c envoycp/envoy-minimal.yaml"],shell=True)
  else:
    print("func-e is not available")
    subprocess.run(["curl https://func-e.io/install.sh | bash -s -- -b /usr/local/bin"],shell=True)
    subprocess.run(["func-e run -c envoycp/envoy-minimal.yaml"],shell=True)
  return HttpResponse("envoy process killed")

@csrf_exempt
def stop_envoy(request):
  subprocess.run(["kill -9 $(pidof func-e)"],shell=True)
  return HttpResponse("envoy stopped")
