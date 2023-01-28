#!/usr/bin/python3
import argparse
import comm
import RPi.GPIO as RPIO

parser = argparse.ArgumentParser()
parser.add_argument(
    "--screenshot",action="store_true",
    help="Request a Screenshot from the calculator"
)
parser.add_argument(
    "--backup",action="store_true",
    help="Backup the calculator"
)
parser.add_argument(
    "--os",action="store_true",
    help="Get FLASH OS"
)
parser.add_argument(
    "--versions",action="store_true",
    help="Request info about calculator OS and Model versions"
)
parser.add_argument(
    "--list",action="store_true",
    help="List all files in calculator memory"
)
parser.add_argument(
    "--request",action="store",
    help="Requests a file from calculator memory"
)
parser.add_argument(
    "--receive",action="store_true",
    help="Receive a file chosen by the calculator"
)
parser.add_argument(
    "-g","--gpio",action="store",
    help="GPIO Pins to use 'L,R' ; default:'6,5'"
)
parser.add_argument(
    "--send",action="store",
    help="Sends a file to calculator memory"
)
args = parser.parse_args()

pins = (6,5)
if args.gpio:
    p = args.gpio.split(",")
    pins = [int(p[0]), int(p[1])]

if args.screenshot:
    comm.screenshot(pins)
if args.backup:
    comm.backup(pins)
if args.os:
    comm.receive_os(pins)
if args.versions:
    comm.versions(pins)
if args.list:
    comm.list_dir(pins)
if args.request:
    comm.request(pins,args.request)
if args.send:
    comm.send(pins,args.send)
if args.receive:
    comm.receive(pins)

RPIO.cleanup()
