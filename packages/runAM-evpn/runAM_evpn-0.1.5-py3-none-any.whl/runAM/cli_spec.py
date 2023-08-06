# The cli_spec is used by runAM.cli to build build argparse arguments.

cli_spec = {
    '__main_parser': {
        'help': '=== runAM (run Arista Module) CLI help ===\n    To enable autocomplete run: eval "$(register-python-argcomplete runAM)"',
        'add_argument': [
            {
                'arg_name': '--echo',
                'arg_short_name': '-e',
                'action': 'store_true',
                'default': True,
                'help': 'Print child module output if available.',
            },
        ]
    },
    # server
    'server.add': {
        'python_module': 'runAM.ServerTicketStore().addServerTicket',
        'help': 'Add server ticket data.',
        'add_argument': [
            {
                'arg_name': '--input_file',
                'arg_short_name': '-inf',
                'help': 'Filename to load input data.',
            },
            {
                'arg_name': '--skip_port_cfg_gen',
                'arg_short_name': '-skip_pcfg',
                'help': 'Generate port configuration data',
                'default': False,
                'action': 'store_true',
            }
        ]
    },
    'server.delete': {
        'python_module': 'runAM.ServerTicketStore().deleteServerTicket',
        'help': 'Delete a server from the database.',
        'add_argument': [
            {
                'arg_name': '--server_id',
                'arg_short_name': '-sid',
                'help': 'Server to be deleted.',
            }
        ]
    },
    'server.query': {
        'python_module': 'runAM.ServerTicketStore().queryServerTicket',
        'help': 'Query server table by server ID.',
        'add_argument': [
            {
                'arg_name': '--server_id',
                'arg_short_name': '-sid',
                'help': 'Find server ticket with specified ID.',
            },
            {
                'arg_name': '--switch_name',
                'arg_short_name': '-sw',
                'help': 'Find server tickets for a specified switch hostname.',
            },
            {
                'arg_name': '--switch_port',
                'arg_short_name': '-port',
                'help': 'Find server tickets for a specified switch port name.',
            },
            {
                'arg_name': '--print_yaml',
                'arg_short_name': '-yml',
                'help': 'Print matched tickets as YAML docs.',
                'default': False,
                'action': 'store_true'
            },
            {
                'arg_name': '--print_docIDs',
                'arg_short_name': '-docID',
                'help': 'Print document IDs for matched tickets. Not printed by default.',
                'default': False,
                'action': 'store_true'
            },
        ]
    },
    # profile
    'profile.add': {
        'python_module': 'runAM.ProfileTicketStore().addProfileTicket',
        'help': 'Add profile ticket data.',
        'add_argument': [
            {
                'arg_name': '--input_file',
                'arg_short_name': '-inf',
                'help': 'Filename to load input data.',
            }
        ]
    },
    'profile.delete': {
        'python_module': 'runAM.ProfileTicketStore().deleteProfileTicket',
        'help': 'Delete a profile from the database.',
        'add_argument': [
            {
                'arg_name': '--tags',
                'arg_short_name': '-t',
                'help': 'Tag list for a profile to be deleted. For example: --tags tag1, tag2, ...',
            }
        ]
    },
    'profile.query': {
        'python_module': 'runAM.ProfileTicketStore().queryProfileTicket',
        'help': 'Query profile table for specific tags.',
        'add_argument': [
            {
                'arg_name': '--tags',
                'arg_short_name': '-t',
                'help': 'Find a profile with specified tags. For example: --tags tag1, tag2, ...',
            }
        ]
    },
    # generators
    'generate.port_config_data': {
        'python_module': 'runAM.generate.PortConfigGenerator().generatePortConfigData',
        'help': 'Generate low level data to parse port configuration templates.',
    },
    # tools
    'tools.time_stamp': {
        'python_module': 'runAM.tools.time_stamp',
        'help': 'Print current time as Y-M-D H-M-S. In case you are lost in time and terminal has no time stamp enabled. =)',
    },
}
