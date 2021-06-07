import requests
import json


async def getParameters(msg):
    try:
        list = msg.split(' ')
        if list[0] == '查梗' and len(list) == 2:
            return [True, list[1]]
    except:
        pass
    return [False]


async def getMessage(bot, userGroup, msg):
    parameter = await getParameters(msg)
    if parameter[0] == False:
        return
    print(parameter[1])
    api_url = 'https://api.jikipedia.com/go/search_definitions'
    api_data = json.dumps(
        {
            "page": 1,
            "phrase": parameter[1]
        }
    )
    api_headers = {
        "Client": "web",
        "Content-Type": "application/json;charset=UTF-8",
        "Origin": "https://jikipedia.com"
    }
    result = json.loads(
        requests.post(
            api_url, data=api_data, headers=api_headers
        ).text
    )

    try:
        title = result["data"][0]["term"]["title"]
    except IndexError:
        await bot.send_group_msg(group_id=userGroup, message="未找到相应词条")
        # print("未找到相应词条")
        return
    r_tags = "标签：无"
    content = result["data"][0]["plaintext"]

    tags = []
    tag_num = 0
    for t in result["data"][0]["tags"]:
        tags.append(t["name"])
        tag_num = tag_num + 1
    if tag_num != 0:
        r_tags = f"标签:" + "|".join(tags)
    if parameter[1] == title:
        msg_text = f"词条：{title}\n{r_tags}\n----------------------\n{content}\n"
    else:
        r_titles = []
        n = 1
        for tit in result["data"]:
            r_titles.append(tit["term"]["title"])
            if n > 7:
                break
            n += 1
        remsg = f"未找到相应词条{msg}\n你可能要找？\n -->" + f"\n -->".join(
            r_titles) + f"\n数据来源为小鸡词典\nhttps://jikipedia.com/\n如果发现任何有问题的词条，与本bot无关，请前往小鸡词典官网反馈。"
        await bot.send_group_msg(group_id=userGroup, message=remsg)
        # print(remsg)
        return
    await bot.send_group_msg(group_id=userGroup, message=msg_text)
    # print(msg_text)
