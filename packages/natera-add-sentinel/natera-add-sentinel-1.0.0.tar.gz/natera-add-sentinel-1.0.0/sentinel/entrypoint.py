#!/usr/bin/env python

import dxpy
import argparse
import sys


def payload(ts, ts_id, ps, ps_id, qc_id):
    data = {
        "run_metrics": [
            {
                "$dnanexus_link": qc_id
            }
        ],
        "data": {
            ts: [
                {
                    "$dnanexus_link": ts_id
                }
            ],
            ps: [
                {
                    "$dnanexus_link": ps_id
                }
            ]
        }
    }
    return data


def sentinel_uploader(payload, target_project, folder, ts, ps):
    details = payload

    name = folder + "_upload_sentinel"
    target_folder = "/data/seq/" + folder + "/"

    dxrecord = dxpy.DXRecord()
    dxrecord.new(project=target_project, name=name, folder=target_folder, details=details,
                 types=['UploadSentinel'],
                 tags=[ts, ps],
                 properties={
                     "runFolder": folder,
                 }
                 )

    dxrecord.close()


def main():
    description = '''
    Creates a sentinel with the given parameters.
    Example:

    sentinel
    -p project-FqvZJQQ2yvVGpF0P88GZpXXX \
    -t YOUR_TOKEN \
    -f PHASEIIRS1A1D_20200414 \
    -ts FDZS-20B123 \
    -ts_id file-XXXYYYZZZ \
    -ps FDZS-20B456 \
    -ps_id file-XXXYYYZZZ \
    -qc_id file-XXXYYYZZZ
    '''

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-p", "--project", type=str, help="Target project")
    parser.add_argument("-t", "--token", type=str, help="Project token")
    parser.add_argument("-f", "--folder", type=str, help="WES plasma sampleId")
    parser.add_argument("-ts", "--tissue_sampe", type=str, help="WES tissue sample name")
    parser.add_argument("-ts_id", "--tissue_sampe_Id", type=str, help="WES tissue sampleId")
    parser.add_argument("-ps", "--plasma_sampe", type=str, help="WES plasma sample name")
    parser.add_argument("-ps_id", "--plasma_sampe_Id", type=str, help="WES plasma sampleId")
    parser.add_argument("-qc_id", "--run_metrics_Id", type=str, help="Run Metrics fileId")

    args = parser.parse_args()

    if len(sys.argv) != 17:
        print('Required arguments are missing.')
        parser.print_help()
        sys.exit()

    project = args.project
    token = args.token
    folder = args.folder
    tissue_sampe = args.tissue_sampe
    tissue_sampe_Id = args.tissue_sampe_Id
    plasma_sampe = args.plasma_sampe
    plasma_sampe_Id = args.plasma_sampe_Id
    run_metrics_Id = args.run_metrics_Id

    dxpy.set_security_context({'auth_token_type': 'Bearer',
                               'auth_token': token})

    sent_payload = payload(tissue_sampe, tissue_sampe_Id, plasma_sampe, plasma_sampe_Id, run_metrics_Id)
    sentinel_uploader(sent_payload, project, folder, tissue_sampe, plasma_sampe)

    print('Sentinel record successfully created!')


if __name__ == '__main__':
    main()
