
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'doc', 'docx'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def A4_BC(num: int):
    if 1 <= num <= 3:
        cost = 3
        return cost
    if 3 <= num < 30:
        cost = 3 + (num - 3) * 0.3
        return cost
    if 30 <= num < 100:
        cost = (29 * 0.3) + (num - 29) * 0.2
        return cost
    if num >= 100:
        cost = (99 * 0.2) + (num - 99) * 0.1
        return cost


def A3_BC(num: int):
    if 1 <= num <= 3:
        cost = 3
        return cost
    if 3 < num < 30:
        cost = 4 + (num - 3) * 0.6
        return cost
    if 30 <= num < 100:
        cost = (29 * 0.6) + (num - 29) * 0.4
        return cost
    if num >= 100:
        cost = (99 * 0.4) + (num - 99) * 0.2
        return cost


def A4_C(num: int):
    if 1 <= num <= 3:
        cost = 2
        return cost
    if 3 <= num < 30:
        cost = 2 + (num - 3) * 0.8
        return cost
    if 30 <= num < 100:
        cost = (29 * 0.6) + (num - 29) * 0.6
        return cost
    if num >= 100:
        cost = (99 * 0.4) + (num - 99) * 0.4
        return cost


def A3_C(num: int):
    if num == 1:
        cost = 3
        return cost
    if 2 <= num < 30:
        cost = 3 + (num - 1) * 0.3
        return cost
    if 30 <= num < 100:
        cost = (29 * 1.6) + (num - 29) * 1.2
        return cost
    if num >= 100:
        cost = (99 * 1.2) + (num - 99) * 0.8
        return cost
