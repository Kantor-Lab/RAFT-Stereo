import os
import demo
import argparse

fx= 1760.466789 
fy= 1759.986350
cx1= 720.366851
cy= 492.207186
cx2= 690.244907
baseline= 60.038 # millimeters

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--restore_ckpt', help="restore checkpoint", required=True)
    parser.add_argument('--save_numpy', action='store_true', help='save output as numpy arrays')
    parser.add_argument('--mixed_precision', action='store_true', help='use mixed precision')
    parser.add_argument('--corr_implementation', choices=["reg", "alt", "reg_cuda", "alt_cuda"], default="reg", help="correlation volume implementation")
    parser.add_argument('--input_directory', type=str, default='', help='input directory to read left/right images from')

    args = parser.parse_args()

    print("Input directory: ", args.input_directory)
    args.output_directory = os.path.join(args.input_directory, 'output')
    left_images = []
    right_images = []
    segmented_images = []

    for file in os.listdir(os.path.join(args.input_directory, 'left')):
        if file.endswith(".png"):
            left_images.append(os.path.join(args.input_directory, 'left', file))
        else:
            continue

    for file in os.listdir(os.path.join(args.input_directory, 'right')):
        if file.endswith(".png"):
            right_images.append(os.path.join(args.input_directory, 'right', file))
        else:
            continue

    for file in os.listdir(os.path.join(args.input_directory, 'outputs')):
        if file.endswith(".jpg"):
            segmented_images.append(file)
        else:
            continue
    
    left_images.sort()
    right_images.sort()

    print("Left images: ", left_images[0])
    print("Right images: ", len(right_images))
    print("Segmented images: ", segmented_images)
    for l, r in zip(left_images, right_images):
        filename =  os.path.splitext(os.path.basename(l))[0] + '_mask.jpg'
        print("Filename: ", filename)
        if filename in segmented_images:
            print("Left image: ", l)
            print("Right image: ", r)
            demo.main(['--restore_ckpt', args.restore_ckpt, '--save_numpy', '--mixed_precision', '--corr_implementation', args.corr_implementation, '--left_imgs', l, '--right_imgs', r, '--output_directory', args.output_directory])
    # for file in os.listdir(args.input_directory):
    #     if file.endswith(".png"):
    #         input_img = os.path.join(args.input_directory, file)
    #         print("Input image: ", input_img)
    #         demo.main(['--config', args.config, '--grounded_checkpoint', args.grounded_checkpoint, '--sam_checkpoint', args.sam_checkpoint, '--input_image', input_img, '--text_prompt', args.text_prompt, '--box_threshold', str(args.box_threshold), '--text_threshold', str(args.text_threshold), '--device', args.device])
    #     else:
    #         continue
