"""AvecAgro soil-sensor client: sends readings to the AvecAgro server's /api/sensor endpoint.

Use it from a Raspberry Pi or laptop wired to a soil probe, or as a reference for an ESP32/Arduino sketch
(the HTTP request is the same). Standard library only.

Examples
  # one reading typed in
  python tools/sensor_device.py --device field-1 --moisture 18 --ph 7.2 --soil-temp 24

  # every 15 minutes, reading values from your own probe function (edit read_probe below)
  python tools/sensor_device.py --device field-1 --every 900

Then type the same sensor ID ("field-1") in the Advisor tab; its latest reading is added to the farm details.
"""
import argparse, json, os, time, urllib.request

def read_probe():
    """Replace with real probe code, e.g. a capacitive moisture sensor on an ADC.
    Return a dict with any of: soil_moisture_pct, soil_ph, soil_temp_c, air_temp_c, humidity_pct, ec_ds_m."""
    raise SystemExit('No probe connected: edit read_probe() or pass values with --moisture/--ph/...')

def send(server, token, payload):
    req = urllib.request.Request(server.rstrip('/') + '/api/sensor', data=json.dumps(payload).encode(),
                                 headers={'content-type': 'application/json', **({'x-sensor-token': token} if token else {})})
    with urllib.request.urlopen(req, timeout=90) as r:
        return json.loads(r.read())

def main():
    a = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    a.add_argument('--server', default=os.environ.get('AVECAGRO_SERVER', 'https://avecagro.onrender.com'))
    a.add_argument('--token', default=os.environ.get('SENSOR_TOKEN', ''), help='only if the server sets SENSOR_TOKEN')
    a.add_argument('--device', required=True)
    a.add_argument('--moisture', type=float, dest='soil_moisture_pct')
    a.add_argument('--ph', type=float, dest='soil_ph')
    a.add_argument('--soil-temp', type=float, dest='soil_temp_c')
    a.add_argument('--air-temp', type=float, dest='air_temp_c')
    a.add_argument('--humidity', type=float, dest='humidity_pct')
    a.add_argument('--every', type=int, default=0, help='seconds between readings (uses read_probe)')
    args = a.parse_args()
    fields = ['soil_moisture_pct', 'soil_ph', 'soil_temp_c', 'air_temp_c', 'humidity_pct']
    typed = {k: getattr(args, k) for k in fields if getattr(args, k) is not None}
    while True:
        values = typed or read_probe()
        out = send(args.server, args.token, {'device': args.device, **values})
        print(time.strftime('%H:%M:%S'), json.dumps(out['stored']))
        if not args.every: break
        time.sleep(args.every)

if __name__ == '__main__':
    main()
