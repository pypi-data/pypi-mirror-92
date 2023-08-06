import os
import io
from django.http.response import HttpResponse
from bs4 import BeautifulSoup
import json
import re
from .scanner import mujocso_location

class MujocsoException(Exception):
    pass

def render(headers=[], elements=[], page_title='Mujocso Page', style=[], using=[], toolsscripts=[], script=[], template=None):
    # Local Functions
    def URL_validation(url):
        regex = re.compile(
            r'^(?:http|ftp)s?://'
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|'
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
            r'(?::\d+)?'
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        
        return re.match(regex, url) is not None
    
    def ListInList(list1, list2):
        for item in list1:
            if(item in list2):
                pass
            else:
                return False
        return True
    #--------------
    global mujocso_location
    allowed_header_inputs = ['value', 'size']
    alowed_element_inputs = ['type', 'value']
    allowed_element_types = ['p', 'a', 'img']
    avaliable_styles = ['CBRORANGE', 'CENTERTITLEORANGE']
    avaliable_page_styles = []
    allowed_toolsscript_files = ['script.js', 'config.json']
    avaliable_templates = ['CBRO404']
    page_body = page_style = page_using = page_scripts = page_toolsscripts = ''
    # Template find validation
    if(template != None):
        if(type(template) == str):
            if(template.upper() in avaliable_templates):
                with io.open(file=mujocso_location+'/template_files/'+str(template).upper()+'.css', encoding='UTF-8') as template_css:
                    template_css = template_css.read()
                page_style = template_css
            else:
                raise MujocsoException('Template not found')
        else:
            raise MujocsoException('Template type is not valid')
    # Styles find validation
    if(style != [] and template == None and type(style) == list):
        for s in style:
            if(s in avaliable_page_styles):
                with io.open(file=mujocso_location+'/template_files/'+str(s).upper()+'.css', encoding='UTF-8') as style_css:
                    style_css = style_css.read()
                    style_css = style_css.replace('*{ /* Mujocso Css Format Start */\n', '')
                    style_css = style_css.replace('\n} /* Mujocso Css Format End */', '')
                    page_style += style_css
            else:
                if(s.endswith(";") == False):
                    page_style += s+';'
                else:
                    page_style += s
    # Add scripts in 'page_scripts'
    if(script != [] and type(script) == list):
        for script_ in script:
            page_scripts += script_+'\n'
    # ToolsScripts find validation
    if(toolsscripts != [] and type(toolsscripts) == list):
        for script_foldername in toolsscripts:
            if(type(script_foldername) == str):
                for root, directory, files in os.walk(mujocso_location+'/addonscript_files/'+str(script_foldername).upper()):
                    if(ListInList(allowed_toolsscript_files, files)):
                        pass
                    else:
                        raise MujocsoException(f'There was a problem processing ({script_foldername}) AddonScript files')
            else:
                raise MujocsoException('ToolsScripts name, must be string')
    #-------------------
    # Headers Validation
    if(type(headers) == list):
        for header in headers:
            if(type(header) == dict):
                for key in allowed_header_inputs:
                    if(key in header and int(header['size']) <= 6):
                        continue
                    else:
                        raise MujocsoException('Header values must be valid')
            else:
                raise MujocsoException('Header values must be a dictionary')
    else:
        raise MujocsoException('The headers type, must be a list')
    # Elements Validation
    if(type(elements) == list):
        for element in elements:
            if(type(element) == dict):
                
                # Fix Img Error Passing Bug
                if(element['type'] == 'img'):
                    alowed_element_inputs.append('src')
                    alowed_element_inputs.append('alt')
                for key in alowed_element_inputs:
                    if(key in element):
                        continue
                    else:
                        raise MujocsoException('Element values must be valid')
            else:
                raise MujocsoException('Element values must be a dictionary')
    else:
        raise MujocsoException('The elements type, must be a list')
    # using Add & Validation
    if(type(using) == list):
        for script in using:
            if(type(script) == str):
                validation = URL_validation(script)
                if(validation):
                    element_tag = 'script'
                    add_to_var = '<'+element_tag+' '+'src="'+script+'"'+' '+'>'
                    page_using += add_to_var
                    page_using += '\n'
                else:
                    raise MujocsoException('using URL must be valid')
            else:
                raise MujocsoException('using values must be a string')
    else:
        raise MujocsoException('The using type, must be a list')
    
    
    with io.open(file=mujocso_location+'/template_files/page.html', encoding='UTF-8') as page:
        o = page.read()
    o = o.replace(
        '{*PAGE_TITLE*}',
        page_title 
        )
    
    # Check And Processing Headers
    if(type(headers) == list):
        for header in headers:
            header_tag = 'h'+str(header['size'])
            styles_temp = ''
            tag_parameters = ''
            if('style' in header):
                if(type(header['style']) == list):
                    for style in header['style']:
                        if(style.upper() in avaliable_styles):
                            with io.open(file=mujocso_location+'/template_files/'+str(style).upper()+'.css', encoding='UTF-8') as style_css:
                                style_css = style_css.read()
                                style_css = style_css.replace('*{ /* Mujocso Css Format Start */\n', '')
                                style_css = style_css.replace('\n} /* Mujocso Css Format End */', '')
                                styles_temp += style_css
                        else:
                            if(style.endswith(";") == False):
                                styles_temp += '\n'+style+';'
                            else:
                                styles_temp += '\n'+style
                    
                elif(type(header['style']) == str):
                    if(header['style'].upper() in avaliable_styles):
                        with io.open(file=mujocso_location+'/template_files/'+str(header['style']).upper()+'.css', encoding='UTF-8') as style_css:
                            style_css = style_css.read()
                            style_css = style_css.replace('*{ /* Mujocso Css Format Start */\n', '')
                            style_css = style_css.replace('\n} /* Mujocso Css Format End */', '')
                            styles_temp += style_css
                    else:
                        if(header['style'].endswith(";") == False):
                            styles_temp += header['style']+';'
                        else:
                            styles_temp += header['style']
                else:
                    raise MujocsoException("The headers style type must be string or list")
                styles_temp = styles_temp.replace('\n', ' ').replace('  ', ' ')
                style_param = 'style="'+styles_temp+'"'
                tag_parameters += ' '+style_param
            if('id' in header):
                id_param = 'id="'+header['id']+'"'
                tag_parameters += ' '+id_param
            if('class' in header):
                class_param = 'class="'+header['class']+'"'
                tag_parameters += ' '+class_param
            
            add_to_body = '<'+header_tag+tag_parameters+'>'+str(header['value'])+'</'+header_tag+'>'
            ## -- Add To Body -- ##
            page_body += add_to_body
            page_body += '\n' 
    if(type(elements) == list):
        for element in elements:
            element_tag = element_value = ''
            element_addons = ' '
            
            if(element['type'] in allowed_element_types):
                # allowed_element_types[0] = <p> Tag
                # if(element['type'] == allowed_element_types[0]):
                element_tag = element['type']
                element_value = element['value']
                
                if(len(element_tag) != 2):
                    element_data_temp = element
                    del element_data_temp['type']
                    del element_data_temp['value']
                    
                    for param, value in element_data_temp.items():
                        element_value = value
                        if(param == 'style'):
                            if(type(value) == str):
                                if(value.endswith(";") == False):
                                    element_value = value+';'
                            elif(type(value) == list):
                                in_cache = ''
                                for script in value:
                                    if(script.endswith(";") == False):
                                        script = script+';'
                                    in_cache += script
                                element_value = in_cache
                            else:
                                raise MujocsoException('Element style type must be a list or a string')
                                    
                        element_addons += param+'="'+str(element_value)+'" '
                add_to_body = '<'+element_tag+element_addons+'>'+element_value+'</'+element_tag+'>'
                page_body += add_to_body
                page_body += '\n' 
            else:
                raise MujocsoException('Element type must be valid')
    
    # ToolsScripts Validation
    if(type(toolsscripts) == list):
        for script in toolsscripts:
            with io.open(file=mujocso_location+'/toolsscript_files/'+script.upper()+'/config.json', encoding='UTF-8') as file:
                script_config = file.read()
            with io.open(file=mujocso_location+'/toolsscript_files/'+script.upper()+'/script.js', encoding='UTF-8') as file:
                script_content = file.read()
            
            script_config = json.loads(script_config) # Load as json
            page_toolsscripts += script_content+'\n\n'+script_config['script_to_add']
    o = o.replace(
        '{*BODY_SPACE*}',
        '<body>\n'+page_body+'\n</body>'
        )
    o = o.replace(
        '{*STYLE_SPACE*}',
        '<style>\n'+page_style+'\n</style>' if page_style != '' else ''
        )
    o = o.replace(
        '{*SCRIPT_SPACE*}',
        '<script>\n'+page_scripts+'\n</script>' if page_scripts != '' else ''
        )
    o = o.replace(
        '{*PAGESCRIPTS_SPACE*}',
        page_scripts if page_using != '' else ''
        )
    o = o.replace(
        '{*TOOLSSCRIPTS_SPACE*}',
        ''
        )
            
    
    soup = BeautifulSoup(o, 'html.parser')
    output = soup.prettify()
    return HttpResponse(output)