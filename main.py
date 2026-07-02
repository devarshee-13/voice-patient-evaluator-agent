import argparse

from call_manager import run_conversation_loop, start_outbound_call
from persona import PATIENT_PERSONAS


def parse_args():
    parser = argparse.ArgumentParser(description="Pretty Good AI patient caller")
    subparsers = parser.add_subparsers(dest="command", required=True)

    for command in ("call", "simulate"):
        subparser = subparsers.add_parser(command)
        subparser.add_argument(
            "--persona",
            choices=PATIENT_PERSONAS.keys(),
            default="scheduler",
            help="Patient persona to use for the call",
        )
        subparser.add_argument(
            "--call-number",
            type=int,
            default=1,
            help="Call number used in transcript filenames",
        )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    if args.command == "call":
        start_outbound_call(args.persona, args.call_number)
    elif args.command == "simulate":
        run_conversation_loop(args.persona, args.call_number)