import genanki
# List of Linux directories and their descriptions
linux_dirs = [
    ('/', 'Root directory, starting point of the filesystem hierarchy.'),
    ('/bin', 'Contains essential system command executables.'),
    ('/sbin', 'Contains essential system administration command executables.'),
    ('/boot', 'Contains files needed to start the boot process.'),
    ('/etc', "Contains system-wide configuration files and scripts."),
    ('/dev', 'Contains device files representing hardware devices.'),
    ('/home', 'Contains personal directories for each user.'),
    ('/lib', 'Contains shared libraries and kernel modules.'),
    ('/opt', 'Optional directory for storing third-party software.'),
    ('/proc', 'Virtual filesystem providing an interface to kernel internal data structures.'),
    ('/sys', 'Virtual filesystem providing an interface to kernel internal data structures for devices, drivers, and other components.'),
    ('/tmp', 'Temporary directory for storing files deleted after a system reboot.'),
    ('/usr', 'Contains user-related files, shared libraries, header files, documentation, and non-essential software binaries.'),
    ('/var', 'Contains variable data files, such as logs, databases, and mail spools.'),
]

# Define Anki note model
model_id = 1607392319
model = genanki.Model(
    model_id,
    'Simple Model',
    fields=[
        {'name': 'Directory'},
        {'name': 'Description'},
    ],
    templates=[
        {
            'name': 'Card 1',
            'qfmt': '{{Directory}}',
            'afmt': '{{Description}}',
        },
        {
            'name': 'Card 2',
            'qfmt': '{{Description}}',
            'afmt': '{{Directory}}',
        },
    ])

# Generate Anki cards and add them to a deck
deck_id = 2059400110
deck = genanki.Deck(deck_id, 'Linux Filesystem')

for dir_name, description in linux_dirs:
    note = genanki.Note(model=model, fields=[dir_name, description])
    deck.add_note(note)

# Save the deck to an Anki package (*.apkg) file
genanki.Package(deck).write_to_file('linux_filesystem.apkg')