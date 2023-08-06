import sys
import os
from pathlib import Path
from dotenv import load_dotenv
from consolebundle.CommandManager import CommandManager
from consolebundle.ConsoleArgumentParser import ConsoleArgumentParser
from pyfonycore.bootstrap.config import configReader

def runCommand():
    argumentsParser = ConsoleArgumentParser()
    argumentsParser.add_argument(dest='commandName')

    envKwargs = dict(required=False, help='Environment')

    if 'APP_ENV' in os.environ:
        envKwargs['default'] = os.environ['APP_ENV']

    argumentsParser.add_argument('-e', '--env', **envKwargs)

    knownArgs = argumentsParser.parse_known_args()[0]

    bootstrapConfig = configReader.read()
    container = bootstrapConfig.containerInitFunction(knownArgs.env, bootstrapConfig)
    commandManager: CommandManager = container.get('consolebundle.CommandManager')

    logger = container.get('consolebundle.logger')
    logger.warning('Running command in {} environment'.format(knownArgs.env.upper()))

    if len(sys.argv) < 2:
        logger.error('Command not specified, example usage: console mynamespace:mycommand')

        print('\n[Available commands]:')

        for existingCommand in commandManager.getCommands():
            logger.info(existingCommand.getCommand() + ' - ' + existingCommand.getDescription())

        sys.exit(1)

    try:
        command = commandManager.getByName(knownArgs.commandName)
    except Exception as e: # pylint: disable = broad-except
        logger.error(str(e))
        sys.exit(1)

    command.configure(argumentsParser)
    argumentsParser.setCommandName(knownArgs.commandName)

    knownArgs = argumentsParser.parse_known_args()[0]
    command.run(knownArgs)

if __name__ == '__main__':
    dotEnvFilePath = Path.cwd() / '.env'

    if dotEnvFilePath.exists():
        load_dotenv(dotenv_path=str(dotEnvFilePath))

    runCommand()
