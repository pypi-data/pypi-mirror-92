"""Python DDNS main entry point"""
from configparser import ConfigParser
import argparse
import os
import sys
import logging
import requests

from .providers import Cloudflare, HurricaneElectric, Strato


def make_logger(name: str, loglevel: str) -> logging.Logger:
    """Makes the logger"""
    logger = logging.getLogger(name)
    logger.setLevel(loglevel)
    formatter = logging.Formatter(
        "%(levelname)s - %(name)s - %(asctime)s - %(message)s", "%Y-%m-%d %H:%M:%S"
    )
    fh = logging.FileHandler("{}.log".format(name), mode="w")
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger


def get_ip() -> str:
    """
    Gets the public ip address of the host system.
    """
    ip = requests.get("https://checkip.amazonaws.com").text.strip()
    return ip


def initialize(log: logging.Logger) -> int:
    """Renames config file"""
    dn = os.path.dirname(os.path.realpath(__file__))
    try:
        os.rename(os.path.join(dn, "config.dist.conf"), os.path.join(dn, "config.conf"))
        log.info("File renamed successfully. " "Path is {}/config.conf".format(dn))
        return 0
    except FileNotFoundError:
        log.info("Error: File not found.\nFiles are: {}".format(os.listdir(dn)))
        return 1


def quick_test(log: logging.Logger, CONF: ConfigParser()) -> int:
    """Tests to make sure the config is readable"""
    dn = os.path.dirname(os.path.realpath(__file__))
    if len(CONF.sections()) == 0:
        log.error("Error: File not found.\nFiles are: {}".format(os.listdir(dn)))
        raise FileNotFoundError("Did not find the configuration file")
    log.debug({section: dict(CONF[section]) for section in CONF.sections()})
    log.debug(get_ip())
    log.info("Test Completed Successfully")
    return 0


def run():
    """
    Main function that does all the work
    """
    __version__ = "v2.1.0"
    parser = argparse.ArgumentParser(prog="pddns", description="DDNS Client")
    parser.add_argument(
        "-t",
        "--test",
        default=False,
        action="store_true",
        help="Tests to make sure the config is readable",
    )
    parser.add_argument(
        "-i",
        "--initialize",
        default=False,
        action="store_true",
        help="Renames the dist config",
    )
    parser.add_argument(
        "-f",
        "--file",
        default="config.conf",
        dest="configfile",
        help="Path to configuration file",
    )
    parser.add_argument(
        "--Cloud", action="store_true", dest="cloud", help="Forces Cloudflare"
    )
    parser.add_argument(
        "--Hurricane",
        action="store_true",
        dest="hurricane",
        help="Forces Hurricane Electric",
    )
    parser.add_argument(
        "--Strato", action="store_true", dest="strato", help="Forces Strato"
    )
    # Logging function from https://stackoverflow.com/a/20663028
    parser.add_argument(
        "-d",
        "--debug",
        help="Sets logging level to DEBUG.",
        action="store_const",
        dest="loglevel",
        const=logging.DEBUG,
        default=logging.WARNING,
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="Sets logging level to INFO",
        action="store_const",
        dest="loglevel",
        const=logging.INFO,
    )
    args = parser.parse_args()

    log = make_logger("PDDNS", args.loglevel)
    log.info("Starting up")
    log.debug(args)

    if args.initialize:
        sys.exit(initialize(log))

    CONFIG = ConfigParser(interpolation=None)
    if args.configfile == "config.conf":
        dn = os.path.dirname(os.path.realpath(__file__))
        CONFIG.read(os.path.join(dn, args.configfile))
    else:
        CONFIG.read(args.configfile)

    if args.test:
        sys.exit(quick_test(log, CONFIG))

    provider = CONFIG.get("Provider", "Provider").lower()

    if args.cloud or provider == "cloudflare":
        client = Cloudflare(CONFIG, __version__)
    if args.hurricane or provider.startswith("hurricane"):
        client = HurricaneElectric(CONFIG, __version__)
    if args.cloud or provider == "strato":
        client = Strato(CONFIG, __version__)
    client.main(get_ip())


if __name__ == "__main__":
    run()
