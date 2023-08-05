import kwimage
from os.path import join, exists, relpath
import os
import pickle
import ubelt as ub
import torchvision
import kwcoco


def convert_cifar_to_coco(dpath=None):
    workdir = ub.expandpath('~/work/cifar')
    DATASET = torchvision.datasets.CIFAR10

    # dset = DATASET(root=workdir, download=True)
    # meta_fpath = os.path.join(dset.root, dset.base_folder, 'batches.meta')
    # meta_dict = pickle.load(open(meta_fpath, 'rb'))
    # classes = meta_dict['label_names']

    DATASET = torchvision.datasets.CIFAR100

    modes = ['train', 'test']

    cifar100_classes = {
        'aquatic_mammal'               : ['beaver', 'dolphin', 'otter', 'seal', 'whale'],
        'fish'                         : ['aquarium_fish', 'flatfish', 'ray', 'shark', 'trout'],
        'flower'                       : ['orchid', 'poppy', 'rose', 'sunflower', 'tulip'],
        'food_container'               : ['bottle', 'bowl', 'can', 'cup', 'plate'],
        'fruit_and_vegetable'          : ['apple', 'mushroom', 'orange', 'pear', 'sweet_pepper'],
        'household_electrical_device'  : ['clock', 'keyboard', 'lamp', 'telephone', 'television'],
        'household_furniture'          : ['bed', 'chair', 'couch', 'table', 'wardrobe'],
        'insect'                       : ['bee', 'beetle', 'butterfly', 'caterpillar', 'cockroach'],
        'large_carnivore'              : ['bear', 'leopard', 'lion', 'tiger', 'wolf'],
        'large_man_made_outdoor_thing' : ['bridge', 'castle', 'house', 'road', 'skyscraper'],
        'large_natural_outdoor_scene'  : ['cloud', 'forest', 'mountain', 'plain', 'sea'],
        'large_omnivore_and_herbivore' : ['camel', 'cattle', 'chimpanzee', 'elephant', 'kangaroo'],
        'medium_sized_mammal'          : ['fox', 'porcupine', 'possum', 'raccoon', 'skunk'],
        'non_insect_invertebrate'      : ['crab', 'lobster', 'snail', 'spider', 'worm'],
        'person'                       : ['baby', 'boy', 'girl', 'man', 'woman'],
        'reptile'                      : ['crocodile', 'dinosaur', 'lizard', 'snake', 'turtle'],
        'small_mammal'                 : ['hamster', 'mouse', 'rabbit', 'shrew', 'squirrel'],
        'tree'                         : ['maple_tree', 'oak_tree', 'palm_tree', 'pine_tree', 'willow_tree'],
        'vehicle_1'                    : ['bicycle', 'bus', 'motorcycle', 'pickup_truck', 'train'],
        'vehicle_2'                    : ['lawn_mower', 'rocket', 'streetcar', 'tank', 'tractor'],
    }
    dpath = ub.ensuredir((workdir, 'cifar-100-coco'))

    for mode in modes:
        cifar = DATASET(root=workdir, download=True, train=(mode == 'train'))
        meta_fpath = os.path.join(cifar.root, cifar.base_folder, 'meta')
        meta_dict = pickle.load(open(meta_fpath, 'rb'))
        classes = meta_dict['fine_label_names']

        _known_catnames = set(ub.flatten(cifar100_classes.values()))
        assert not (set(classes) - set(_known_catnames))
        assert not print(set(_known_catnames) - set(classes))

        img_root = ub.ensuredir((dpath, '{}_images'.format(mode)))

        fine_to_dpath = {}
        for parent, children in cifar100_classes.items():
            for child in children:
                fine_dpath = ub.ensuredir((img_root, parent, child))
                fine_to_dpath[child] = fine_dpath

        dset = kwcoco.CocoDataset(img_root=img_root)
        dset.fpath = join(dpath, 'cifar100_{}.kwcoco.json'.format(mode))

        for parent, children in cifar100_classes.items():
            dset.add_category(parent)
            for child in children:
                dset.add_category(child, supercategory=parent)

        for idx in ub.ProgIter(range(len(cifar.data)), desc='write images'):
            imdata = cifar.data[idx]
            cidx = cifar.targets[idx]
            label = classes[cidx]
            item_dpath = fine_to_dpath[label]
            item_fpath = join(item_dpath, 'cifar100_{}_{:05}.png'.format(mode, idx))

            rel_fpath = relpath(item_fpath, dpath)
            gid = dset.add_image(rel_fpath)
            cid = dset.name_to_cat[label]['id']
            dset.add_annotation(image_id=gid, bbox=[0, 0, 32, 32],
                                width=32, height=32, category_id=cid)

            if not exists(item_fpath):
                kwimage.imwrite(item_fpath, imdata)

        dset.dump(dset.fpath, newlines=True)
