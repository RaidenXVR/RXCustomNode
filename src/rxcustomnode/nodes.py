from inspect import cleandoc
import comfy
import folder_paths


class RXCustomInput:
    """
    A example node

    Class methods
    -------------
    INPUT_TYPES (dict):
        Tell the main program input parameters of nodes.
    IS_CHANGED:
        optional method to control when the node is re executed.

    Attributes
    ----------
    RETURN_TYPES (`tuple`):
        The type of each element in the output tulple.
    RETURN_NAMES (`tuple`):
        Optional: The name of each output in the output tulple.
    FUNCTION (`str`):
        The name of the entry-point method. For example, if `FUNCTION = "execute"` then it will run Example().execute()
    OUTPUT_NODE ([`bool`]):
        If this node is an output node that outputs a result/image from the graph. The SaveImage node is an example.
        The backend iterates on these output nodes and tries to execute all their parents if their parent graph is properly connected.
        Assumed to be False if not present.
    CATEGORY (`str`):
        The category the node should appear in the UI.
    execute(s) -> tuple || None:
        The entry point method. The name of this method must be the same as the value of property `FUNCTION`.
        For example, if `FUNCTION = "execute"` then this method's name must be `execute`, if `FUNCTION = "foo"` then it must be `foo`.
    """

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        """
        Return a dictionary which contains config for all input fields.
        Some types (string): "MODEL", "VAE", "CLIP", "CONDITIONING", "LATENT", "IMAGE", "INT", "STRING", "FLOAT".
        Input types "INT", "STRING" or "FLOAT" are special values for fields on the node.
        The type can be a list for selection.

        Returns: `dict`:
            - Key input_fields_group (`string`): Can be either required, hidden or optional. A node class must have property `required`
            - Value input_fields (`dict`): Contains input fields config:
                * Key field_name (`string`): Name of a entry-point method's argument
                * Value field_config (`tuple`):
                    + First value is a string indicate the type of field or a list for selection.
                    + Secound value is a config for type "INT", "STRING" or "FLOAT".
        """
        return {
            "required": {
                "model_name": (
                    folder_paths.get_filename_list("checkpoints"),
                    {"tooltip": "The name of the checkpoint (model) to load."},
                ),
                "prompt": (
                    "STRING",
                    {"multiline": True, "default": "masterpiece, best quality, 1girl"},
                ),
                "negative_prompt": ("STRING", {"multiline": True, "default": ""}),
            },
            "optional": {
                "sampler": (comfy.samplers.KSampler.SAMPLERS,),
                "scheduler": (comfy.samplers.KSampler.SCHEDULERS,),
                "steps": ("INT", {"default": 25, "min": 1, "max": 150, "step": 1}),
                "cfg": (
                    "FLOAT",
                    {"default": 5.0, "min": 0.0, "max": 20.0, "step": 0.1},
                ),
                "seed": (
                    "INT",
                    {"default": -1, "min": -1, "max": 2147483647, "step": 1},
                ),
                "width": ("INT", {"default": 1024, "min": 64, "max": 2048, "step": 64}),
                "height": (
                    "INT",
                    {"default": 1536, "min": 64, "max": 2048, "step": 64},
                ),
            },
        }

    @classmethod
    def IS_CHANGED(
        cls,
        model_name,
        prompt,
        negative_prompt,
        sampler,
        scheduler,
        steps,
        cfg,
        seed,
        width,
        height,
    ):
        print("RXCustomInput IS_CHANGED called")
        return f"{model_name}-{prompt}-{negative_prompt}-{sampler}-{scheduler}-{steps}-{cfg}-{seed}-{width}-{height}"

    RETURN_TYPES = (
        folder_paths.get_filename_list("checkpoints"),
        "STRING",
        "STRING",
        comfy.samplers.KSampler.SAMPLERS,
        comfy.samplers.KSampler.SCHEDULERS,
        "INT",
        "FLOAT",
        "INT",
        "INT",
        "INT",
    )

    RETURN_NAMES = (
        "model_name",
        "prompt",
        "negative_prompt",
        "sampler",
        "scheduler",
        "steps",
        "cfg",
        "seed",
        "width",
        "height",
    )

    DESCRIPTION = cleandoc(__doc__)
    FUNCTION = "test"

    # OUTPUT_NODE = False
    # OUTPUT_TOOLTIPS = ("",) # Tooltips for the output node

    CATEGORY = "Custom Nodes"

    def test(
        self,
        model_name,
        prompt,
        negative_prompt,
        sampler,
        scheduler,
        steps,
        cfg,
        seed,
        width,
        height,
    ):

        print(
            f"""Your input contains:
            model_name: {model_name}
            prompt: {prompt}
            negative_prompt: {negative_prompt}
            sampler: {sampler}
            scheduler: {scheduler}
            steps: {steps}
            cfg: {cfg}
            seed: {seed}
            width: {width}
            height: {height}
            """
        )

        return (
            model_name,
            prompt,
            negative_prompt,
            sampler,
            scheduler,
            steps,
            cfg,
            seed,
            width,
            height,
        )

    """
        The node will always be re executed if any of the inputs change but
        this method can be used to force the node to execute again even when the inputs don't change.
        You can make this node return a number or a string. This value will be compared to the one returned the last time the node was
        executed, if it is different the node will be executed again.
        This method is used in the core repo for the LoadImage node where they return the image hash as a string, if the image hash
        changes between executions the LoadImage node is executed again.
    """
    # @classmethod
    # def IS_CHANGED(s, image, string_field, int_field, float_field, print_to_screen):
    #    return ""


# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {"RXCustomInput": RXCustomInput}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {"RXCustomInput": "RX Custom Input Node"}
