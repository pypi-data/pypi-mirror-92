from nomnomdata.engine.components import Parameter, ParameterGroup, SharedConfig
from nomnomdata.engine.parameters import Code, Enum, Nested, String

FirebaseToDatabase = SharedConfig(
    shared_config_type_uuid="FB2DB-NND3C",
    description="Firebase collection to a relational database table configuration parameters.",
    alias="Firebase to Relational Database",
    categories=[
        "Firebase",
        "Loader",
        "Relational Database",
    ],
    parameter_groups=[
        ParameterGroup(
            Parameter(
                name="collection_name",
                display_name="Collection",
                description="Name of the collection in the Firebase app.",
                type=String(max=1024),
                required=True,
            ),
            Parameter(
                name="tracking_field",
                display_name="Tracking Field",
                description="Name of the field in the Collection to use for sorting and tracking documents processed.",
                required=False,
                type=String(),
            ),
            Parameter(
                name="tracking_field_type",
                display_name="Tracking Field Type",
                description="Select the data type of the Tracking Field.",
                required=False,
                type=Enum(choices=["NONE", "DATETIME", "STRING", "PUSHID"]),
                default="NONE",
            ),
            name="collection_parameters",
            display_name="Collection Parameters",
            description="Collection configuration information.",
        ),
        ParameterGroup(
            Parameter(
                name="load_pattern",
                display_name="Load Pattern",
                description="Select the pattern to use when loading the data.",
                type=Enum(choices=["INSERT"]),
                default="INSERT",
            ),
            Parameter(
                name="documentid_field",
                display_name="DocumentId Column",
                description="Map the DocumentId field to this column in the relational database.  Add a column with the same name to Column Parameters below.",
                type=String(),
                required=False,
            ),
            Parameter(
                name="date_processed_column",
                display_name="Date Processed Column",
                description="If specified, a date column representing when data was processed will be added to the relational database. Add a column with the same name to Column Parameters below.",
                type=String(),
                required=False,
            ),
            name="load_parameters",
            display_name="Load Parameters",
            description="Options for loading data into the relational database.",
        ),
        ParameterGroup(
            Parameter(
                name="column_parameters",
                display_name="Column Parameters",
                description="Details about each column within the relational database.",
                required=True,
                many=True,
                type=Nested(
                    Parameter(
                        name="column_name",
                        display_name="Column Name",
                        description="Specify the name of the column.",
                        type=String(max=128),
                        required=True,
                    ),
                    Parameter(
                        name="column_type",
                        display_name="Column Data Type",
                        description="Select the data type of the column. If type selected is not supported, the closest matching type will be used.",
                        type=Enum(
                            choices=[
                                "VARCHAR",
                                "INTEGER",
                                "BIGINT",
                                "DATETIME",
                                "DATE",
                                "TIME",
                                "TIMESTAMP",
                                "BOOLEAN",
                                "NUMERIC",
                                "FLOAT",
                                "BYTES",
                                "ARRAY",
                                "STRUCT",
                                "GEOGRAPHY",
                                # STRING
                            ]
                        ),
                        required=True,
                    ),
                    Parameter(
                        name="column_config",
                        display_name="Column Configuration",
                        description="Specify a configuration for the column. For example, VARCHAR could be (128), NUMERIC could be (12,2), ARRAY could be <STRING>, STRUCT could be <DATE, STRING>.",
                        type=String(),
                        required=False,
                    ),
                    Parameter(
                        name="json_path",
                        display_name="JSON Path",
                        description="Firebase field to map to the column. For example, ['store']['book']['title'] or store.book.title.",
                        type=String(),
                        required=False,
                    ),
                ),
            )
        ),
        ParameterGroup(
            Parameter(
                name="custom_parameter",
                display_name="Custom Parameters",
                description="Specify each parameter and value in quotes, separated by a colon.  Separate each pair with a comma and enclose all of the pairs in curly braces.",
                type=Code(),
                required=False,
            ),
            name="additional_parameters",
            display_name="Additional Parameters",
            description="Any additional parameters not described above.",
        ),
    ],
)


S3FileToDatabase = SharedConfig(
    shared_config_type_uuid="S3BTK-DB3MD",
    description="Metadata for files stored on S3. Provide information needed when data from the files is loaded into other relational systems.",
    alias="S3 File to Relational Database",
    categories=[
        "S3",
        "Loader",
        "Relational Database",
    ],
    parameter_groups=[
        ParameterGroup(
            Parameter(
                name="bucket",
                display_name="Bucket",
                description="Select the S3 bucket containing the files.",
                type=String(max=1024),
                required=True,
            ),
            Parameter(
                name="path",
                display_name="Path",
                description="Specify the path to the files within the S3 bucket.",
                type=String(max=2048),
                required=False,
            ),
            name="location_parameters",
            display_name="Location Parameters",
            description="Information used to locate the files the metadata applies to.",
        ),
        ParameterGroup(
            Parameter(
                name="load_pattern",
                display_name="Load Pattern",
                description="Select the pattern to use when loading the data.",
                type=Enum(choices=["INSERT"]),
                default="INSERT",
            ),
            Parameter(
                name="file_type",
                display_name="Data Format",
                description="Select the format of the data in the files.",
                type=Enum(choices=["JSON", "Delimited"]),
                default="JSON",
            ),
            Parameter(
                name="compression",
                display_name="Compression Format",
                description="Select the compression, if any, applied to the files.",
                type=Enum(choices=["None", "gzip", "zip", "bzip"]),
                default="None",
            ),
            Parameter(
                name="delimiter",
                display_name="Delimiter",
                description="Specify the character used to separate data values in files with delimited data format.",
                type=String(max=2),
                required=False,
            ),
            Parameter(
                name="null_value",
                display_name="Null Value",
                description="Specify the characters used to represent a null value in files with delimited data format.",
                type=String(max=8),
                required=False,
            ),
            Parameter(
                name="escape_character",
                display_name="Escape Character",
                description="Specify the character used to represent an escaped value in files with delimited data format.",
                type=String(max=2),
                required=False,
            ),
            name="load_parameters",
            display_name="Load Parameters",
            description="Options for loading data into the relational database.",
        ),
        ParameterGroup(
            Parameter(
                name="distribution_key",
                display_name="Partition Key",
                description="Specify the name of the single column whose values will be used to partition each file's data.",
                type=String(max=1024),
                required=True,
            ),
            Parameter(
                name="sort_key",
                display_name="Sort Key",
                description="Specify one or more names, with commas between each name, whose values will be used to sort each file's data.",
                type=String(max=2048),
                required=False,
            ),
            name="key_parameters",
            display_name="Key Parameters",
            description="Columns used to partition, sort, merge and de-duplicate data with named columns.",
        ),
        ParameterGroup(
            Parameter(
                name="column_parameters",
                display_name="Column Parameters",
                description="Details about each column within the relational database.",
                required=True,
                many=True,
                type=Nested(
                    Parameter(
                        name="column_name",
                        display_name="Column Name",
                        description="Specify the name of the column.",
                        type=String(max=128),
                        required=True,
                    ),
                    Parameter(
                        name="column_type",
                        display_name="Column Data Type",
                        description="Select the data type of the column. If type selected is not supported, the closest matching type will be used.",
                        type=Enum(
                            choices=[
                                "VARCHAR",
                                "INTEGER",
                                "BIGINT",
                                "DATETIME",
                                "DATE",
                                "TIME",
                                "TIMESTAMP",
                                "BOOLEAN",
                                "NUMERIC",
                                "FLOAT",
                                "BYTES",
                                "ARRAY",
                                "STRUCT",
                                "GEOGRAPHY",
                                # STRING
                            ]
                        ),
                        required=True,
                    ),
                    Parameter(
                        name="column_config",
                        display_name="Column Configuration",
                        description="Specify a configuration for the column. For example, VARCHAR could be (128), NUMERIC could be (12,2), ARRAY could be <STRING>, STRUCT could be <DATE, STRING>.",
                        type=String(),
                        required=False,
                    ),
                    Parameter(
                        name="json_path",
                        display_name="JSON Path",
                        description="Firebase field to map to the column. For example, ['store']['book']['title'] or store.book.title.",
                        type=String(),
                        required=False,
                    ),
                ),
            )
        ),
        ParameterGroup(
            Parameter(
                name="custom_parameter",
                display_name="Custom Parameters",
                description="Specify each parameter and value in quotes, separated by a colon.  Separate each pair with a comma and enclose all of the pairs in curly braces.",
                type=Code(),
                required=False,
            ),
            name="additional_parameters",
            display_name="Additional Parameters",
            description="Any additional parameters not described above.",
        ),
    ],
)
