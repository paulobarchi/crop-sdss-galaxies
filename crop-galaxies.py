import argparse
import pandas as pd
import numpy as np
from math import fabs
from os import path
import astropy.io.fits as pyfits
import matplotlib.pyplot as plt
import matplotlib.colors as colors


def saveImgFromFitsData(file_name, data):
    plt.imshow(data, cmap='gray', norm=colors.LogNorm(
        vmin=np.median(data),vmax=np.percentile(data,98)))
    plt.box(False)
    plt.tick_params(
            axis='both',
            which='both',
            bottom=False,
            top=False,
            labelbottom=False,
            right=False,
            left=False,
            labelleft=False)
    plt.savefig(file_name, bbox_inches='tight')
    plt.clf()


def main():
    parser = argparse.ArgumentParser(
            description="Crop galaxies' stamps from Fields")
    parser.add_argument("-i", "--input_csv", type=str, required=True,
            help="csv input file with necessary info")
    parser.add_argument("-d", "--input_dir", type=str, required=True,
            help="input directory with Fields")
    parser.add_argument("-Rp", "--rp", type=int, required=True,
            help="Size in Rp for each stamp. Let's say you input 5 here,\
                the size of each stamp will be 5*Rp", default=5)
    parser.add_argument("-o", "--output_dir", type=str, required=True,
            help="output directory for saving stamps")
    parser.add_argument('--save_png', dest='save_png', action='store_true')
    parser.add_argument('--not_save_png', dest='save_png', action='store_false')
    parser.set_defaults(save_png=True)

    args = parser.parse_args()

    half_size = float(args.rp/2.0)

    df = pd.read_csv(args.input_csv)

    for index, row in df.iterrows():
        objId = row['ObjId'].astype(int)
        out_count = out_count + 1

        field_file_string = "fpC-%06d-%c%d-%04d.fit" % (
                int(row['run']), "r", int(row['camcol']), int(row['field']))

        field_file_name = path.join(args.input_dir, field_file_string)

        data = pyfits.getdata(field_file_name, 0)

        # checking stamp size and boundaries
        sdss_rp = float(row['petroRad_r'])
        rowc, colc = float(row['rowc_r']), float(row['colc_r'])
        size_x = np.min(np.array(
            [fabs(colc), args.rp*sdss_rp, fabs(data.shape[1]-colc)]
            ))
        size_y = np.min(np.array(
            [fabs(rowc), args.rp*sdss_rp, fabs(data.shape[0]-rowc)]
            ))

        size = int(np.min(np.array([size_x, size_y])))

        x = int(colc)
        y = int(rowc)
        data = data[y-size:y+size+1, x-size:x+size+1]

        out_full_path = path.join(args.output_dir, str(objId))

        outfits = pyfits.PrimaryHDU(data=data)
        outfits.writeto(out_full_path+".fit", overwrite=True)

        if (args.save_png):
            saveImgFromFitsData(out_full_path+".png", data)


if __name__ == '__main__':
    main()
