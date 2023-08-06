# See documentation on http://experimaestro.github.io/datamaestro/

from datamaestro.definitions import datatasks, datatags, dataset
from datamaestro.data import Base


@datatags("image", "celebrities")
@dataset(Base, url="http://mmlab.ie.cuhk.edu.hk/projects/CelebA.html", id="")
def __main__():
    """large-scale face attributes dataset with more than 200K celebrity images, each with 40 attribute annotations

    CelebFaces Attributes Dataset (CelebA) is a large-scale face attributes dataset with more than 200K celebrity images, each with 40 attribute annotations. The images in this dataset cover large pose variations and background clutter. CelebA has large diversities, large quantities, and rich annotations, including

      - 10,177 number of identities,
      - 202,599 number of face images, and
      - 5 landmark locations, 40 binary attributes annotations per image.

    The dataset can be employed as the training and test sets for the following computer vision tasks: face attribute recognition, face detection, landmark (or facial part) localization, and face editing & synthesis.
    """
    return {}
