---
layout: post
title: "Automatically load avro schemas that reference other schemas"
tags:
 - python
 - avro
meta-description: 
# Don't change the disqus identifier even if the url changes. It uniquely
# associates comments with the post.
disqus-identifier: "automatically_load_avro_schemas_that_reference_other_schemas"
summary: A method for automatically loading avro schemas that reference schema in separate files.
---

<!-- excerpt start -->
This post demonstrates a method for how one might automatically load avro schemas that reference schemas stored in separate files.
<!-- excerpt end -->

This approach was useful for working on a legacy system in which we were investigating the usefulness of changing the messaging from an internally defined serialisation format to avro. 

The legacy system used a message oriented architecture consisting of thousands of different request/reply messages. The messages generally followed a common structure of a header and a body. The body is constructed of various scalar and composite types. The types used within messages are also used in application code and hence are needed as separate files during application compilation. However,  when constructing a message it would be useful to simply load a single schema.

By default avro does not understand that a schema is defined in a separate file. This typically needs to be built into application code.

Internet searches show examples of constructing avro schemas with references to schemas in separate files. However, when using these schemas the example code always seemed to load the low level referenced schemas first - implying some upfront knowledge about dependency order.

This (otherwise very useful) example from [gisgeek](http://gisgeek.blogspot.com.au/2012/12/using-apache-avro-with-python.html) demonstrates the pre-loading of low level schemas.

So one method to avoid this problem would be to simply load all system types in order from low level up to the higher level message structures. This is possible, we know the dependency order. However we would like to avoid unnecessarily loading types that are not going to be used.

The method I used to automatically load schemas, without needing to have earlier loaded up the lower level schemas is as follows:

{% highlight python %}

import json
import os
from avro import schema

def load_schema(file_path, names=None):
    '''
    Load a schema file and return a schema object. The schema can
    reference other schemas and all these will be loaded into the
    names object too.

    This function attempts to load the specified schema. If avro
    detects an error it raises an exception that we catch and
    inspect to find the cause.

    If the cause is because of an unresolved dependency we inspect
    the error to determine the appropriate file to load that contains
    the schema and then try to load the original schema again.

    If the cause is because the type is already specified within the
    names object we ignore it because this situation arises from us
    having previously attempted to load the type - but failed due a
    dependency error.

    file_path: path to schema file
    names(optional): avro.schema.Names object
    '''
    schema_file = os.path.basename(file_path)
    schema_dir = os.path.dirname(file_path)
    print "Loading %s" % schema_file

    with open(file_path) as f:
        json_data = json.loads(f.read())
        while True:

            try:

                loaded_schema = schema.make_avsc_object(json_data, names)

            except schema.SchemaParseException as ex:

                if ex.message.startswith("The name ") and ex.message.endswith(" is already in use."):
                    type_name = ex.message.split("\"")[1]
                    # This error can happen while we are trying to recursively
                    # re-load a type but encountering dependency isses.
                    # Ignore this error by removing the name clash and reloading
                    # the schema.
                    del names.names[type_name]
                    loaded_schema = schema.make_avsc_object(json_data, names)
                    break
                else:
                    # An exception is typically raised due to a problem with
                    # the schema. This is normally because of a reference to
                    # a separate schema that this schema depends on.
                    #
                    # Extract content between quotes which should be the type
                    # name that is not resolving. In line with assumption '1'
                    # this type name should match the .avsc file that we need
                    # to load to resolve this particular problem.

                    item_name_with_namespace = ex.message.split("\"")[1]
                    item_name = item_name_with_namespace.split(".")[-1]
                    print "Loading %s dependency %s" % (schema_file, item_name)
                    dependency_schema_file = os.path.join(schema_dir,
                                                          "%s.avsc" % item_name)
                    load_schema(dependency_schema_file, names)

        return loaded_schema


def flatten(schema_object):
    empty_names = schema.Names()
    schema_content = schema_object.to_json(empty_names)
    schema_file_content = json.dumps(schema_content, indent=2)
    return schema_file_content


def main():
    '''
    Process a top level schema inro a flattened version.
    '''
    TEST_SCHEMA_FILE = 'example_msg.avsc'
    names = schema.Names()
    schema_object = load_schema(TEST_SCHEMA_FILE, names)
    flattened_schema_file = "flattened_%s" % TEST_SCHEMA_FILE
    with open(flattened_schema_file, 'w') as fd:
        fd.write(flatten(schema_object))


if __name__ == "__main__":
    main()

{% endhighlight %}

The loading mechanism simply catches the exceptions from loading the top level schema and inspects the error to determine the dependency file to load. This is performed recursively until the schema is loaded.

Additionally, the script generates a flattened version of the schema. By flat I mean that it does not contain references to other schemas.

Having a flat schema available means that, once processed, only one file needs to be loaded, rather than having to implement some form of knowledgable wrapper that will load schemas in the approriate order.

To test this method, create the following files in the same directory as the code script:

executable.avsc
{% highlight javascript %}
{
    "type": "record",
    "name": "executable",
    "namespace": "a_namespace",
    "fields": [
        {"name": "identifier", "type": ["string", "null"]},
        {"name": "instance" , "type": ["int", "null"]}
    ]
}
{% endhighlight %}

header.avsc
{% highlight javascript %}
{
    "type": "record",
    "name": "header",
    "namespace": "a_namespace",
    "fields": [
        {"name": "msg_id", "type": ["int", "null"]},
        {"name": "priority" , "type": ["int", "null"]},
        {"name": "source" , "type": "a_namespace.executable"},
        {"name": "target" , "type": "a_namespace.executable"}
    ]
}
{% endhighlight %}

example_msg.avsc
{% highlight javascript %}
{
    "type": "record",
    "namespace": "a_namespace",
    "name": "Example_Msg",
    "fields": [
        {"name": "header", "type": "a_namespace.header"},
        {"name": "age", "type": ["int", "null"]},
        {"name": "address", "type": ["string", "null"]},
        {"name": "value", "type": ["long", "null"]}
    ]
}
{% endhighlight %}

These avro schemas define an example message that depends on a header schema which in turn depends on a executable schema. 

The script will load the top level schema, example_msg, without needing the manually load up the lower level schemas first. It then writes out a flattened version to ```flattened_example_msg.avsc```.

In the legacy system the flattened schema versions are quite large and for the time being could not reliablly be edited by hand. So while the flatteded versions are useful in the application when loading the schema to create or decode a message it seems likely that the many base types would remain in their own files because it is easier to modify smaller structures.

The next item to look into is the avro IPC to investigate sending messages between applications without the schema overhead for every message transaction.
