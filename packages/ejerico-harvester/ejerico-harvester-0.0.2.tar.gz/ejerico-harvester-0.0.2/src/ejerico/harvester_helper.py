"""TODO doc"""

import collections
import itertools
import mimetypes
import os
import re

import atoma
import netCDF4
import numpy as np
import requests

import rdflib

from datetime import datetime
from dateutil.relativedelta import relativedelta

from url_decode import urldecode

from geopy.geocoders import Nominatim

from SPARQLWrapper import SPARQLWrapper, JSON, TURTLE

from ejerico_sdk.utils import isPrimitive, tokenize_name
from ejerico_sdk.rdf.graph_factory import GraphFactory
from ejerico_sdk.rdf.entity import ConceptSchema, Concept

class HarvesterHelper(object):

    DEFAULT_MIMETYPE = "application/unknown"

    def __init__(self):
        object.__init__(self)

    def parseDatetime(self, date_string, date_format='%Y-%m-%d %H:%M:%S'):
        return datetime.strptime(date_string, date_format)

    def has_attribute(self, obj, *attributes):
        rst = self.get_attribute(obj, attributes) is not None

    def get_attribute(self, obj, *attributes):
        value = None

        exists = obj is not None and attributes is not None
        if exists: 
            value = obj
            for attribute in attributes:
                if not isinstance(attribute,str): return None

                if isinstance(value, collections.OrderedDict):
                    exists = exists and attribute in value
                    value = value[attribute] if exists else None
                elif isinstance(value, dict):
                    exists = exists and attribute in value
                    value = value[attribute] if exists else None
                else:
                    exists = exists and attribute in value.__dict__
                    value = value.__dict__[attribute] if exists else None

        return value if exists else None

    def nameToID(self, name):
        rst = self.generateIDsFromName(name)
        return rst[0] if rst is not None else None
    
    def generateIDsFromName(self, name, remove_punctuation=True, min_terms=-1, left_coincidences=1):
        return tokenize_name(name, remove_punctuation=remove_punctuation, min_terms=min_terms, left_coincidences=left_coincidences)   

    def guessMimetype(self, url):
        rst = mimetypes.guess_type(urldecode(url.replace('-','_')))
        return self.DEFAULT_MIMETYPE if rst[0] == None else rst[0]

    def getAndParseAtomFile(self, url=None, session=None, headers=None):
        feed = None

        try:
            if url is not None:
                requests_params = {"url": url}
                if headers is not None: requests_params["headers"] = headers

                response = requests.get(**requests_params)
                if requests.codes.ok == response.status_code:
                    feed = atoma.parse_atom_bytes(response.content)
        except Exception as e:
            print("TODO handle exception")
        
        return feed

    def getAndParseRSSFile(self, url=None):
        feed = None

        try:
            response = requests.get(url=url)
            if requests.codes.ok == response.status_code:
                feed = atoma.parse_rss_bytes(response.content)
        except Exception as e:
            print("TODO handle exception")
        
        return feed

    def numpy_to_scalar(self, nc_val):
            for dtype in self.numpy_to_scalar.dtypes:
                if isinstance(nc_val, dtype): 
                    return nc_val.item()

            if isinstance(nc_val, np.ndarray): 
                return nc_val.tolist()

            return nc_val

    numpy_to_scalar.dtypes = (
        np.int8,np.int16,np.int32,np.int64,
        np.uint8,np.uint16,np.uint32,np.uint64,
        np.intp,np.uintp,
        np.float32,np.float64)

    def doResourceAnalysis(self, mimetype=None, url=None):
        print("[HarvesterHelper::doResourceAnalysis] Entering method ({})".format(mimetype))
        if "application/x-netcdf" == mimetype:
            return self._doResourceAnalysis_netcdf(url)
        return {}
    
    def _doResourceAnalysis_netcdf(self, url):
        def nc_process_variable(nc_name, nc_var):
            proc_var = {}
            for nc_attr in nc_var.ncattrs():
                nc_val = nc_var.getncattr(nc_attr)
                proc_var[nc_attr] = self.numpy_to_scalar(nc_val)

            if "actual_range" in proc_var:
                proc_var["{}_min".format(nc_name)] = proc_var["actual_range"][0]
                proc_var["{}_max".format(nc_name)] = proc_var["actual_range"][-1]
            
            return proc_var

        data = {}
        try:
            with netCDF4.Dataset(url) as nc:
                for attr in nc.__dict__:
                    if isPrimitive(nc.__dict__[attr]):
                        data[attr] = nc.__dict__[attr]

                nc_variables = {}
                for nc_var_key in nc.variables.keys():
                    nc_var_val = nc.variables[nc_var_key]
                    for d in nc_var_val.dimensions:
                        nc_var_key = re.sub("^{}.".format(d),"",nc_var_key)
                    nc_variables[nc_var_key] = nc_process_variable(nc_var_key, nc_var_val) 
                    
                data["variables"] = nc_variables

                print("[HarvesterHelper::_doResourceAnalysis] TODO process netcdf4 file ({})".format(url))
        except ImportError as e:
            print("[HarvesterHelper::_doResourceAnalysis] error importing netcdf4 file ({}) -> {}".format(url, e))
        except Exception as e:
            print("[HarvesterHelper::_doResourceAnalysis] error processing netcdf4 file ({}) -> {}".format(url, e))
        
        return data

    def doProcessKnowSourceURL(self, url):
        print("[HarvesterHelper::doProcessKnowSourceURL] Entering method ({})".format(url))

        #TODO case: handle.net (https://github.com/EUDAT-B2SAFE/B2HANDLE)
        pass

        #TODO case: doi.org (https://www.doi.org/factsheets/DOIProx.html#rest-api)
        pass

        #TODO case: ORCID (https://github.com/ORCID/python-orcid)
        pass

        #TODO case: BODC (http://vocab.nerc.ac.uk/collection/???/current/???/)
        if re.match(self.doProcessKnowSourceURL.re_BODC_1, url):
            return self.doProcessKnowSourceURL_BODC(url)
        if re.match(self.doProcessKnowSourceURL.re_BODC_2, url):
            return self.doProcessKnowSourceURL_BODC(url)

        #TODO case: EDMO (https://edmo.seadatanet.org/sparql/)
        if re.match(self.doProcessKnowSourceURL.re_EDMO, url):
            return self.doProcessKnowSourceURL_EDMO(url)
        #TODO case: EDMERP (https://edmerp.seadatanet.org/sparql/)
        if re.match(self.doProcessKnowSourceURL.re_EDMERP, url):
            return self.doProcessKnowSourceURL_EDMERP(url)

        #TODO case: WMO (https://cpdb.wmo.int/data/institutionalinformation)
        pass
    doProcessKnowSourceURL.re_BODC_1 = re.compile(r"http://vocab.nerc.ac.uk/collection/(\w)+/current/(\w)+/")
    doProcessKnowSourceURL.re_BODC_2 = re.compile(r"SDN:(?P<scheme>\w+)::(?P<concept>\w+)")
    doProcessKnowSourceURL.re_EDMO = re.compile(r"EDMO:(?P<edmo>\w+)")
    doProcessKnowSourceURL.re_EDMERP = re.compile(r"EDMO:(?P<edmo>\w+)")
    
    def doProcessKnowSourceURL_EDMO(self, url):
        pass
    doProcessKnowSourceURL_EDMO.url_sparql = "https://edmo.seadatanet.org/sparql/"
    doProcessKnowSourceURL_EDMO.uri_pattern = "https://edmo.seadatanet.org/report/{edmo}"
    doProcessKnowSourceURL_EDMO.cache = {}
    doProcessKnowSourceURL_EDMO.namespaces = {}
    doProcessKnowSourceURL_EDMO.map = {}

    def doProcessKnowSourceURL_EDMERP(self, url):
        pass
    doProcessKnowSourceURL_EDMERP.url_sparql = "https://edmerp.seadatanet.org/sparql/"
    doProcessKnowSourceURL_EDMERP.uri_pattern = "https://edmerp.seadatanet.org/report/{edmerp}"
    doProcessKnowSourceURL_EDMERP.cache = {}
    doProcessKnowSourceURL_EDMERP.namespaces = {}
    doProcessKnowSourceURL_EDMERP.map = {}

    def doProcessKnowSourceURL_BODC(self, url):
        if not url.startswith("https://vocab.nerc.ac.uk"):
            m = re.match(self.doProcessKnowSourceURL_BODC.re_BODC, url)
            if not m: return None
            m = m.groups()
            url = "http://vocab.nerc.ac.uk/collection/{}/current/{}/".format(m[0], m[1]) 

        if url in self.doProcessKnowSourceURL_BODC.cache: return self.doProcessKnowSourceURL_BODC.cache[url]
        
        query = "SELECT ?p ?o WHERE { <###URL###> ?p ?o }".replace("###URL###", url)
        sparql = SPARQLWrapper("https://vocab.nerc.ac.uk/sparql/sparql")
        sparql.setReturnFormat(JSON)
        sparql.setQuery(query)
        try :
            data = sparql.query().convert() 
            if "results" in data and "bindings" in data["results"]:
                concept = Concept(first_born=True)
                concept.id = url
                for item in data["results"]["bindings"]:
                    val_p = item["p"]["value"]
                    val_o = item["o"]["value"]
                    if val_p in self.doProcessKnowSourceURL_BODC.namespaces:
                        qname = self.doProcessKnowSourceURL_BODC.namespaces[val_p]
                    else:
                        qname = self.graph.qname(val_p)
                        self.doProcessKnowSourceURL_BODC.namespaces[val_p] = qname
                    if qname in self.doProcessKnowSourceURL_BODC.map:
                        qname = self.doProcessKnowSourceURL_BODC.map[qname]
                        if hasattr(concept, qname) and getattr(concept,qname) is not None:
                            val_p = getattr(concept,qname)
                            if not isinstance(val_p, list): 
                                val_p = [val_p]
                            if val_o not in val_p:
                                val_p.append(val_o)
                            setattr(concept,qname,val_p)
                            setattr(concept,"_empty", False)
                        else:
                            setattr(concept, qname, val_o)
                            setattr(concept,"_empty", False)
                if hasattr(concept, "_empty"):
                    self.doProcessKnowSourceURL_BODC.cache[url] = concept
                    concept.inscheme = None
                    concept.related = None
                    return concept
            else:
                print("[helper:doProcessKnowSourceURL_BODC] empty information for {}".format(url))
        except Exception as e: 
            print(e)
        
        return None

    doProcessKnowSourceURL_BODC.re_BODC = re.compile(r"SDN:(?P<scheme>\w+)::(?P<concept>\w+)")
    doProcessKnowSourceURL_BODC.cache = {}
    doProcessKnowSourceURL_BODC.namespaces = {}
    doProcessKnowSourceURL_BODC.map = {
       "skos:related": "related",
       "skos:definition": "definition",
       "skos:note": "note",
       "dcterms:identifier": "alias",
       "dc:identifier": "alias",
       "skos:prefLabel": "pref_label",
       "skos:altLabel": "alt_label",
       "skos:notation": "notation",
    }

    def get_geoLocation(self, location, nominatim="ejerico"):
        if nominatim not in self.get_geoLocation.cache_nominatim:
            self.get_geoLocation.cache_nominatim[nominatim] = Nominatim(user_agent=nominatim)
        app = self.get_geoLocation.cache_nominatim[nominatim]
        location = app.geocode(location)
        return location.raw if location is not None else location
    get_geoLocation.cache_nominatim = {}

    def list_intersection(self, lstA, lstB):
        lstAB = [a for a in lstA for b in lstB if a == b]
        return lstAB
        
    @property
    def graph(self):
        return self._graph
    @graph.setter
    def graph(self, value):
        self._graph = value
