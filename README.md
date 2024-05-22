# Entity-Relations-Storage

It is an application that stores and queries a huge amount of entities 
and its relations extracted from news.

Entities are categorized into seven main labels as the following:

* Person
* Organization
* Country
* Location
* Time
* Event
* Agreement

At the moment, these following relations are considered as valid 
in the application:

* person meets person
* person/organization organizes an event
* country signed agreement with another country
* person/organization joins organization/event/agreement
* event happens in location/country 
* event happens at time
* person/country agrees with country/event/agreement
* person/country objects country/event/agreement
* person/country cancels event/agreement
* person speaks at event
* person/country negotiate with person/country

The data are stored and managed by Neo4J - a graph database engine.
