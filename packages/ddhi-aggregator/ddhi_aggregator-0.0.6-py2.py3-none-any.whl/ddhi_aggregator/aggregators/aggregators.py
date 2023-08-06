# -*- coding: utf-8 -*-
# aggregators.py
from ddhi_aggregator.entities.entities import Place, Person, Org, Event
from ddhi_encoder.interview import Interview
import xml.etree.ElementTree as ET
from lxml import etree
from importlib import resources
import logging
import os

logger = logging.getLogger(__name__)


class Aggregator:
    def __init__(self, input_dir, output_dir):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.interviews = []
        self.places = []
        self.persons = []
        self.orgs = []
        self.events = []

    def aggregate(self):
        for f in os.listdir(os.path.abspath(self.input_dir)):
            if f.endswith(".tei.xml"):
                interview = Interview()
                interview.read(os.path.join(self.input_dir, f))
                self.include(interview)

    def dump_interviews(self):
        print(etree.tostring(self.formatted_interviews(), pretty_print=True,
                             encoding='unicode'))

    def dump_places(self):
        print(etree.tostring(self.formatted_places(), pretty_print=True,
                             encoding='unicode'))

    def aggregate_place(self, place):
        if not any(p.same_as(place) for p in self.places):
            self.places.append(place)

    def aggregate_person(self, person):
        if not any(p.same_as(person) for p in self.persons):
            self.persons.append(person)

    def aggregate_org(self, org):
        if not any(p.same_as(org) for p in self.orgs):
            self.orgs.append(org)

    def aggregate_event(self, event):
        if not any(p.same_as(event) for p in self.events):
            self.events.append(event)

    def include(self, interview):
        self.interviews.append(interview)
        [self.aggregate_place(Place(place)) for place in interview.places()]
        [self.aggregate_person(Person(person)) for person in interview.persons()]
        [self.aggregate_org(Org(org)) for org in interview.orgs()]
        [self.aggregate_event(Event(event)) for event in interview.events()]

    def transform(self, xsl, xml):
        try:
            result = xsl(xml)
        except etree.XMLSyntaxError as e:
            logger.error(e)
        if result:
            tree = ET.ElementTree(bytes(result))
            root = tree.getroot()
            return etree.fromstring(root)

    def formatted_interview(self, interview):
        return self.transform(self.interview_stylesheet, interview.tei_doc)

    def formatted_place(self, place):
        root = etree.Element("place")
        if place.name:
            name = etree.Element("name")
            name.text = place.name
            root.append(name)
        for k, v in place.idno.items():
            id = etree.Element("id", type=k)
            id.text = v
            root.append(id)
        if place.coordinates:
            location = etree.Element("location")
            location.text = place.coordinates
            root.append(location)
        return root

    def formatted_person(self, person):
        root = etree.Element("person")
        if person.name:
            name = etree.Element("name")
            name.text = person.name
            root.append(name)
        for k, v in person.idno.items():
            id = etree.Element("id", type=k)
            id.text = v
            root.append(id)
        return root

    def formatted_org(self, org):
        root = etree.Element("org")
        if org.name:
            name = etree.Element("name")
            name.text = org.name
            root.append(name)
        for k, v in org.idno.items():
            id = etree.Element("id", type=k)
            id.text = v
            root.append(id)
        return root

    def formatted_event(self, event):
        root = etree.Element("event")
        if event.description:
            name = etree.Element("name")
            name.text = event.description
            root.append(name)
        for k, v in event.idno.items():
            id = etree.Element("id", type=k)
            id.text = v
            root.append(id)
        return root

    def formatted_interviews(self):
        interviews = etree.Element("interviews")
        for interview in self.interviews:
            interview = self.formatted_interview(interview)
            interviews.append(interview)
        return interviews

    def formatted_places(self):
        places = etree.Element("named_places")
        for place in self.places:
            if len(place.idno.items()) > 0:
                place = self.formatted_place(place)
                places.append(place)
        return places

    def formatted_persons(self):
        persons = etree.Element("named_persons")
        for person in self.persons:
            if len(person.idno.items()) > 0:
                person = self.formatted_person(person)
                persons.append(person)
        return persons

    def formatted_orgs(self):
        orgs = etree.Element("named_orgs")
        for org in self.orgs:
            if len(org.idno.items()) > 0:
                org = self.formatted_org(org)
                orgs.append(org)
        return orgs

    def formatted_events(self):
        events = etree.Element("named_events")
        for event in self.events:
            if len(event.idno.items()) > 0:
                event = self.formatted_event(event)
                events.append(event)
        return events

    def export(self):
        self.export_interviews()
        self.export_persons()
        self.export_places()
        self.export_events()

    def export_interviews(self):
        tree = etree.ElementTree(self.formatted_interviews())
        tree.write(os.path.join(self.output_dir, 'Interviews.xml'),
                   pretty_print=True, xml_declaration=True, encoding='utf-8')

    def export_persons(self):
        tree = etree.ElementTree(self.formatted_persons())
        tree.write(os.path.join(self.output_dir, 'Persons.xml'),
                   pretty_print=True, xml_declaration=True, encoding='utf-8')

    def export_places(self):
        tree = etree.ElementTree(self.formatted_places())
        tree.write(os.path.join(self.output_dir, 'Places.xml'),
                   pretty_print=True, xml_declaration=True, encoding='utf-8')

    def export_orgs(self):
        tree = etree.ElementTree(self.formatted_orgs())
        tree.write(os.path.join(self.output_dir, 'Orgs.xml'),
                   pretty_print=True, xml_declaration=True, encoding='utf-8')

    def export_events(self):
        tree = etree.ElementTree(self.formatted_events())
        tree.write(os.path.join(self.output_dir, 'Events.xml'),
                   pretty_print=True, xml_declaration=True, encoding='utf-8')


class AggregatorFactory:
    def aggregator_for(self, project, input_dir, output_dir):
        if project == "DDHI":
            aggregator = Aggregator(input_dir, output_dir)
            with resources.path("xsl", "ddhi-tei2repo.xsl") as xslt_path:
                try:
                    xslt = etree.parse(str(xslt_path))
                except etree.XMLSyntaxError as e:
                    logger.error(e)
            aggregator.interview_stylesheet = etree.XSLT(xslt)
            return aggregator
