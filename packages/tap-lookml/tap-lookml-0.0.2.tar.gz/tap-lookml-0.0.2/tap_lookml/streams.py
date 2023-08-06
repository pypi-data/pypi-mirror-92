# streams: API URL endpoints to be called
# properties:
#   <root node>: Plural stream name for the endpoint
#   path: API endpoint relative path, when added to the base URL, creates the full path,
#       default = stream_name
#   key_properties: Primary key fields for identifying an endpoint record.
#   replication_method: INCREMENTAL or FULL_TABLE
#   replication_keys: bookmark_field(s), typically a date-time, used for filtering the results
#        and setting the state
#   params: Query, sort, and other endpoint specific parameters; default = {}
#   data_key: JSON element containing the results list for the endpoint; default = 'results'
#   bookmark_query_field: From date-time field used for filtering the query

STREAMS = {
    'model_files': {
        'search_path': 'search/code?q=filename:.model.+extension:lkml+repo:[GIT_OWNER]/[GIT_REPOSITORY]',
        'file_path': 'repos/[GIT_OWNER]/[GIT_REPOSITORY]/contents/[GIT_FILE_PATH]',
        'data_key': 'items',
        'key_properties': ['git_owner', 'git_repository', 'path'],
        'replication_method': 'INCREMENTAL',
        'replication_keys': ['last_modified'],
        'bookmark_query_field': 'If-Modified-Since',
        'children': {
            'models': {
                'key_properties': ['git_owner', 'git_repository', 'path'],
                'replication_method': 'FULL_TABLE',
                'parent': 'model_file'
            }
        }
    },
    'view_files': {
        'search_path': 'search/code?q=filename:.view.+extension:lkml+repo:[GIT_OWNER]/[GIT_REPOSITORY]',
        'file_path': 'repos/[GIT_OWNER]/[GIT_REPOSITORY]/contents/[GIT_FILE_PATH]',
        'data_key': 'items',
        'key_properties': ['git_owner', 'git_repository', 'path'],
        'replication_method': 'INCREMENTAL',
        'replication_keys': ['last_modified'],
        'bookmark_query_field': 'If-Modified-Since',
        'children': {
            'views': {
                'data_key': 'views',
                'key_properties': ['git_owner', 'git_repository', 'path', 'name'],
                'replication_method': 'FULL_TABLE',
                'parent': 'view_file'
            }
        }
    }
}

# De-nest children nodes for Discovery mode
def flatten_streams():
    flat_streams = {}
    # Loop through parents
    for stream_name, endpoint_config in STREAMS.items():
        flat_streams[stream_name] = {
            'key_properties': endpoint_config.get('key_properties'),
            'replication_method': endpoint_config.get('replication_method'),
            'replication_keys': endpoint_config.get('replication_keys')
        }
        # Loop through children
        children = endpoint_config.get('children')
        if children:
            for child_stream_name, child_endpoint_config in children.items():
                flat_streams[child_stream_name] = {
                    'key_properties': child_endpoint_config.get('key_properties'),
                    'replication_method': child_endpoint_config.get('replication_method'),
                    'replication_keys': child_endpoint_config.get('replication_keys')
                }
    return flat_streams
