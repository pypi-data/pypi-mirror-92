import os
import Mujocso

javascript_files = html_files = css_files = font_files = toolsscript_files = []

mujocso_location = Mujocso.__file__
mujocso_location = mujocso_location.replace("\\","/")
mujocso_location = mujocso_location.split("/")
mujocso_location.pop()
mujocso_location = '/'.join(mujocso_location)

allowed_font_formats = ['ttf', 'otf', 'eot', 'woff2', 'woff']

for root, directory, files in os.walk(mujocso_location+'/template_files'):
    for file in files:
        if(file.endswith('.js')):
            javascript_files.append(file)

        elif(file.endswith('.html')):
            html_files.append(file)

        elif(file.endswith('.css')):
            css_files.append(file)

        for font_name in allowed_font_formats:
            if(file.endswith('.'+str(font_name))):
                font_files.append(file)
        
        else:
            continue

for root, directory, files in os.walk(mujocso_location+'/toolsscript_files'):
    for script in directory:
        toolsscript_files.append(script)

data_list = {
    'javascript_files':javascript_files,
    'html_files':html_files,
    'css_files':css_files,
    'font_files':font_files,
    'toolsscript_files':toolsscript_files
}