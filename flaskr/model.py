from flask import Blueprint, Response, request, g, jsonify, abort, stream_with_context
import os
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from emoji import emojize

bp = Blueprint("model", __name__)

model = None
tokenizer = None
#model = None
#tokenizer = None


def get_top_3(prediction):
    arr = prediction.logits.numpy()[0]
    best3 = arr.argsort()[-3:][::-1]

    return {0: emojize(l2a[best3[0]]),
            1: emojize(l2a[best3[1]]),
            2: emojize(l2a[best3[2]])}


@bp.route("/initialise")
def initialise():
    global model
    global tokenizer

    if not model or not tokenizer:
        base = os.path.dirname(__file__)
        data = os.path.join(base, 'data')

        model = AutoModelForSequenceClassification.from_pretrained(data)
        model.eval()

        tokenizer = AutoTokenizer.from_pretrained(data)
        
    return jsonify({'status': 'Ready'})


@bp.route("/predict")
def predict():
    if not model or not tokenizer:
        return jsonify(error = 'Model not initialised'), 503

    query = request.args.get('input')
    if query is None:
        return jsonify(error='No input provided'), 400

    # prediction
    inputs = tokenizer(query, return_tensors='pt')
    with torch.no_grad():
        prediction = model(**inputs)

    best3 = get_top_3(prediction)
    return jsonify(best3)


l2a = {
    0: ':smiling_face_with_smiling_eyes:',
    1: ':purple_heart:',
    2: ':backhand_index_pointing_down:',
    3: ':rolling_on_the_floor_laughing:',
    4: ':clapping_hands:',
    5: ':raised_fist:',
    6: ':growing_heart:',
    7: ':trophy:',
    8: ':winking_face:',
    9: ':folded_hands:',
    10: ':backhand_index_pointing_right:',
    11: ':birthday_cake:',
    12: ':woman_dancing:',
    13: ':yellow_heart:',
    14: ':high_voltage:',
    15: ':face_blowing_a_kiss:',
    16: ':winking_face_with_tongue:',
    17: ':camera_with_flash:',
    18: ':blue_heart:',
    19: ':red_heart:',
    20: ':thumbs_up:',
    21: ':fire:',
    22: ':thinking_face:',
    23: ':squinting_face_with_tongue:',
    24: ':collision:',
    25: ':raising_hands:',
    26: ':kiss_mark:',
    27: ':weary_face:',
    28: ':oncoming_fist:',
    29: ':two_hearts:',
    30: ':face_with_rolling_eyes:',
    31: ':smirking_face:',
    32: ':grinning_face:',
    33: ':OK_hand:',
    34: ':sparkling_heart:',
    35: ':sparkles:',
    36: ':loudly_crying_face:',
    37: ':person_shrugging:',
    38: ':flushed_face:',
    39: ':victory_hand:',
    40: ':party_popper:',
    41: ':grinning_squinting_face:',
    42: ':eyes:',
    43: ':grinning_face_with_big_eyes:',
    44: ':musical_notes:',
    45: ':sign_of_the_horns:',
    46: ':camera:',
    47: ':sun:',
    48: ':heart_suit:',
    49: ':see-no-evil_monkey:',
    50: ':soccer_ball:',
    51: ':face_with_tears_of_joy:',
    52: ':basketball:',
    53: ':face_screaming_in_fear:',
    54: ':hundred_points:',
    55: ':smiling_face_with_sunglasses:',
    56: ':grimacing_face:',
    57: ':grinning_face_with_smiling_eyes:',
    58: ':smiling_face:',
    59: ':hugging_face:',
    60: ':beaming_face_with_smiling_eyes:',
    61: ':flexed_biceps:',
    62: ':smiling_face_with_heart-eyes:',
    63: ':green_heart:',
}
