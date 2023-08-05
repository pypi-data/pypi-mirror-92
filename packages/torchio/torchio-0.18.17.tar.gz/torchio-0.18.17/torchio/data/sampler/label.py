from typing import Dict, Optional

import torch

from ...data.image import LabelMap
from ...data.subject import Subject
from ...typing import TypePatchSize
from ...constants import TYPE, LABEL
from .weighted import WeightedSampler


class LabelSampler(WeightedSampler):
    r"""Extract random patches with labeled voxels at their center.

    This sampler yields patches whose center value is greater than 0
    in the :attr:`label_name`.

    Args:
        patch_size: See :class:`~torchio.data.PatchSampler`.
        label_name: Name of the label image in the subject that will be used to
            generate the sampling probability map. If ``None``, the first image
            of type :attr:`torchio.LABEL` found in the subject subject will be
            used.
        label_probabilities: Dictionary containing the probability that each
            class will be sampled. Probabilities do not need to be normalized.
            For example, a value of ``{0: 0, 1: 2, 2: 1, 3: 1}`` will create a
            sampler whose patches centers will have 50% probability of being
            labeled as ``1``, 25% of being ``2`` and 25% of being ``3``.
            If ``None``, the label map is binarized and the value is set to
            ``{0: 0, 1: 1}``.
            If the input has multiple channels, a value of
            ``{0: 0, 1: 2, 2: 1, 3: 1}`` will create a
            sampler whose patches centers will have 50% probability of being
            taken from a non zero value of channel ``1``, 25% from channel
            ``2`` and 25% from channel ``3``.

    Example:
        >>> import torchio as tio
        >>> subject = tio.datasets.Colin27()
        >>> subject
        Colin27(Keys: ('t1', 'head', 'brain'); images: 3)
        >>> subject = tio.SubjectsDataset([subject])[0]
        >>> sampler = tio.data.LabelSampler(64, 'brain')
        >>> generator = sampler(subject)
        >>> for patch in generator:
        ...     print(patch.shape)

    If you want a specific number of patches from a volume, e.g. 10:

        >>> generator = sampler(subject, num_patches=10)
        >>> for patch in iterator:
        ...     print(patch.shape)

    """
    def __init__(
            self,
            patch_size: TypePatchSize,
            label_name: Optional[str] = None,
            label_probabilities: Optional[Dict[int, float]] = None,
            ):
        super().__init__(patch_size, probability_map=label_name)
        self.label_probabilities_dict = label_probabilities

    def get_probability_map_image(self, subject: Subject) -> LabelMap:
        if self.probability_map_name is None:
            for image in subject.get_images(intensity_only=False):
                if image[TYPE] == LABEL:
                    label_map = image
                    break
            else:
                images = subject.get_images(intensity_only=False)
                message = (
                    f'No label maps found in subject {subject} with image'
                    f' paths {[image.path for image in images]}'
                )
                raise RuntimeError(message)
        elif self.probability_map_name in subject:
            label_map = subject[self.probability_map_name]
        else:
            message = (
                f'Image "{self.probability_map_name}"'
                f' not found in subject subject: {subject}'
            )
            raise KeyError(message)
        return label_map

    def get_probability_map(self, subject: Subject) -> torch.Tensor:
        label_map_tensor = self.get_probability_map_image(subject).data
        label_map_tensor = label_map_tensor.float()

        if self.label_probabilities_dict is None:
            return label_map_tensor > 0
        probability_map = self.get_probabilities_from_label_map(
            label_map_tensor,
            self.label_probabilities_dict,
        )
        return probability_map

    @staticmethod
    def get_probabilities_from_label_map(
            label_map: torch.Tensor,
            label_probabilities_dict: Dict[int, float],
            ) -> torch.Tensor:
        """Create probability map according to label map probabilities."""
        multichannel = label_map.shape[0] > 1
        probability_map = torch.zeros_like(label_map)
        label_probs = torch.Tensor(list(label_probabilities_dict.values()))
        normalized_probs = label_probs / label_probs.sum()
        iterable = zip(label_probabilities_dict, normalized_probs)
        for label, label_probability in iterable:
            if multichannel:
                mask = label_map[label]
            else:
                mask = label_map == label
            label_size = mask.sum()
            if not label_size:
                continue
            prob_voxels = label_probability / label_size
            if multichannel:
                probability_map[label] = prob_voxels * mask
            else:
                probability_map[mask] = prob_voxels
        if multichannel:
            probability_map = probability_map.sum(dim=0, keepdim=True)
        return probability_map
