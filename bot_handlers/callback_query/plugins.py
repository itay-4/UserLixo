from config import plugins
from utils import info
from pyrogram import Client, filters
from pyromod.helpers import ikb
from pyromod.nav import Pagination

@Client.on_callback_query(filters.sudoers & filters.regex('^list_plugins (?P<page>\d+)'))
async def onplugins(c,cq):
    lang = cq.lang
    this_page = int(cq.matches[0]['page'])
    
    item_format = 'info_plugin {} {}'
    page_format = 'list_plugins {}'
    if cq.data.endswith('start'):
        item_format = 'info_plugin {} {} start'
        page_format = 'list_plugins {} start'
    
    page = Pagination(
        [*plugins.items()],
        item_data=lambda i, pg: item_format.format(i[0], pg),
        item_title=lambda i, pg: i[0],
        page_data=lambda pg: page_format.format(pg)
    )
    
    lines = page.create(this_page, lines=4, columns=1)
    total = len(lines)
    for n,line in enumerate(lines):
        if n == total-1:
            break
        btn = line[0]
        data = re.match('info_plugin (?P<plugin>.+) (?P<pg>\d+)', btn[1])
        line.append( ('?', f"switch_plugin {data['plugin']} {data['pg']}") )
    
    if cq.message:
        lines.append([(lang.add_plugin, f'add_plugin {this_page} start')])
    else:
        lines.append([(lang.add_plugin, f"t.me/{info['bot']['username']}?start=add_plugin", 'url')])
    if cq.data.endswith('start'):
        lines.append([(lang.back, 'start')])
    else:
        lines.append([(lang.back, 'help')])
    
    await cq.edit(lang.plugins_text, ikb(lines))

@Client.on_callback_query(filters.sudoers & filters.regex('^info_plugin (?P<plugin>.+) (?P<pg>\d+)'))
async def onshowplugin(c,cq):
    lang = cq.lang
    plugin = cq.matches[0]['plugin']
    pg = int(cq.matches[0]['pg'])
    
    if plugin not in plugins:
        return await cq.answer('UNKNOWN')
    
    info = plugins[plugin]
    
    back_data = f'list_plugins {pg}'
    if cq.data.endswith('start'):
        back_data += ' start'
    
    kb = ikb([
        [(lang.back, back_data)]
    ])
    text = lang.plugin_info
    text.escape_html = False
    await cq.edit(text(plugin=plugin, info=info), kb)