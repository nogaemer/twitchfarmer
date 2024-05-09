def img_html(src):
    return "<img src=\"" + src + "\" style=\"width: inherit;border-radius: 20px;\" alt=\"\">"


def title_html(text):
    return ("<p style=\"font-size: 25px;margin: 0;text-align: center;font-family: 'Manrope', sans-serif;font-weight: "
            "bold;\">") + text + "</p>"


def button_html(item_id, channel_id):
    return ("<button style=\"border: medium; border-radius: 20px;padding: "
            "10px;background-color:#24a0ed;cursor:pointer\" onClick=\"execute('" + channel_id + "', '" + item_id +
            "')\">Redeem</button>")
