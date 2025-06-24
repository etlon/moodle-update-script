import io
import os
import shutil
import time
import zipfile
import requests
from requests import get
import hashlib


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_ok(message) -> None:
    print(f'[{bcolors.OKGREEN}OK{bcolors.ENDC}] {message}')


def print_fail(message) -> None:
    print(f'[{bcolors.FAIL}FAIL{bcolors.ENDC}] {message}')


def print_warning(message) -> None:
    print(f'[{bcolors.WARNING}WARNING{bcolors.ENDC}] {message}')


def print_info(message) -> None:
    print(f'[{bcolors.OKBLUE}INFO{bcolors.ENDC}] {message}')


def print_colored(message, color) -> None:
    print(f'{color}{message}{bcolors.ENDC}')


def print_divider(message: str) -> None:
    # divider should be length 40, message should be centered
    divider_length = 40
    message_length = len(message)
    if message_length >= divider_length:
        print_colored(message, bcolors.BOLD)
    else:
        padding_length = divider_length - message_length
        left_padding = padding_length // 2
        right_padding = padding_length - left_padding
        padded_message = '=' * left_padding + message + '=' * right_padding
        print_colored(padded_message, bcolors.BOLD)


def download_and_extract_zip(url: str, extract_to: str) -> None:
    response = requests.get(url, stream=True, headers=headers)
    response.raise_for_status()  # Fehler werfen, wenn Download fehlschlägt

    with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
        zip_ref.extractall(extract_to)


def get_plugin_pathname_tupel(component: str) -> str:
    plugin_types_dict = {
        "mod": "/mod/",
        "antivirus": "/lib/antivirus/",
        "assignsubmission": "/mod/assign/submission/",
        "assignfeedback": "/mod/assign/feedback/",
        "booktool": "/mod/book/tool/",
        "customfield": "/customfield/field/",
        "datafield": "/mod/data/field/",
        "datapreset": "/mod/data/preset/",
        "ltisource": "/mod/lti/source/",
        "fileconverter": "/files/converter/",
        "ltiservice": "/mod/lti/service/",
        "mlbackend": "/lib/mlbackend/",
        "forumreport": "/mod/forum/report/",
        "quiz": "/mod/quiz/report/",
        "quizaccess": "/mod/quiz/accessrule/",
        "scormreport": "/mod/scorm/report/",
        "workshopform": "/mod/workshop/form/",
        "workshopallocation": "/mod/workshop/allocation/",
        "workshopeval": "/mod/workshop/eval/",
        "block": "/blocks/",
        "qtype": "/question/type/",
        "qbehaviour": "/question/behaviour/",
        "qformat": "/question/format/",
        "filter": "/filter/",
        "editor": "/lib/editor/",
        "atto": "/lib/editor/atto/plugins/",
        "enrol": "/enrol/",
        "auth": "/auth/",
        "tool": "/admin/tool/",
        "logstore": "/admin/tool/log/store/",
        "availability": "/availability/condition/",
        "calendartype": "/calendar/type/",
        "message": "/message/output/",
        "format": "/course/format/",
        "dataformat": "/dataformat/",
        "profilefield": "/user/profile/field/",
        "report": "/report/",
        "coursereport": "/course/report/",
        "gradeexport": "/grade/export/",
        "gradeimport": "/grade/import/",
        "gradereport": "/grade/report/",
        "gradingform": "/grade/grading/form/",
        "mnetservice": "/mnet/service/",
        "webservice": "/webservice/",
        "repository": "/repository/",
        "portfolio": "/portfolio/",
        "search": "/search/engine/",
        "media": "/media/player/",
        "plagiarism": "/plagiarism/",
        "cachestore": "/cache/stores/",
        "cachelock": "/cache/locks/",
        "theme": "/theme/",
        "local": "/local/",
        "contenttype": "/contentbank/contenttype/",
        "h5plib": "/h5p/h5plib/",
        "qbank": "/question/bank/",
        "tiny": "/lib/editor/tiny/plugins/",
    }
    # format_banane_test
    plugin_type, plugin_name = component.split("_", 1)
    return plugin_types_dict.get(plugin_type)


def get_files_in_folder(folder_path: str) -> list[str]:
    return [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]


def filename_to_path(name: str) -> str:
    base, ext = os.path.splitext(name)
    parts = base.split('-')
    *dirs, filename = parts
    new_filename = filename + ext
    return os.path.join(*dirs, new_filename)


def create_dict_from_list(files: list[str]) -> dict[str, str]:
    fileset = set(files)
    return {
        default_name: default_name.replace(".default", "")
        for default_name in files
        if default_name.endswith(".default") and default_name.replace(".default", "") in fileset
    }


plugin_list: list[str] = [
    "mod_attendance",
    "mod_choicegroup",
    "mod_customcert",
    "mod_etherpadlite",
    "mod_diary",
    "mod_hvp",
    "mod_journal",
    "mod_lightboxgallery",
    "mod_organizer",
    "mod_publication",
    "mod_reservation",
    "mod_rocketchat",
    "mod_studentquiz",
    "block_onlinesurvey",
    "block_openai_chat",
    "block_panopto",
    "block_xp",
    "qtype_coderunner",
    "qtype_essaywiris",
    "qtype_kprime",
    "qtype_matchwiris",
    "qtype_multianswerwiris",
    "qtype_multichoicewiris",
    "qtype_regexp",
    "qtype_shortanswerwiris",
    "qtype_truefalsewiris",
    "qtype_wq",
    "qbehaviour_adaptive_adapted_for_coderunner",
    "qbehaviour_regexpadaptivewithhelp",
    "qbehaviour_regexpadaptivewithhelpnopenalty",
    "qformat_h5p",
    "filter_h5p",
    "filter_wiris",
    "tiny_wiris",
    "enrol_xp",
    "availability_xp",
    "format_tiles",
    "local_wirisquizzes",
]

# =================== Download Moodle ===================

plugin_api = "https://download.moodle.org/api/1.3/pluginfo.php"
moodle_api = "https://download.moodle.org/api/1.3/updates.php"

payload = 'format=json&version=2024051700&branch=4.4&plugins=mod_quiz%402023110800'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    "Upgrade-Insecure-Requests": "1", "DNT": "1",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate"
}

data = requests.get(moodle_api, params=payload, headers=headers)
moodle_selection = data.json()["updates"]["core"]
releases = [entry['release'] for entry in moodle_selection]

print_info('Available Moodle releases:')
for i, release in enumerate(releases):
    print(f'{bcolors.OKGREEN}[{i}]{bcolors.ENDC} {release}')

release_input = input(
    "Please select a release by entering the corresponding number (0 to {}): ".format(len(releases) - 1))
selected_release = moodle_selection[int(release_input)]
print_info(f'You selected release: {selected_release["release"]}')
download_url = selected_release["download"]
dl_request = get(download_url, allow_redirects=True, headers=headers)
print_divider("Download Moodle")
print_info(f'Downloading Moodle')
with open("moodle.zip", "wb") as f:
    f.write(dl_request.content)
print_ok('Download completed')
print_info(f'Unpacking Moodle')
shutil.unpack_archive("moodle.zip")
print_ok('Unpacking completed')

# =================== Download Plugins ===================
print_divider("Download Plugins")
for plugin in plugin_list:
    # print_info(f'Downloading plugin: {plugin}')
    installation_path_plugin = get_plugin_pathname_tupel(plugin)
    full_plugin_path = "moodle" + installation_path_plugin
    os.makedirs(full_plugin_path, exist_ok=True)
    data = {
        "plugin": f'{plugin}',
        "branch": selected_release["branch"],
        "format": "json"
    }
    server_response = requests.get(plugin_api, params=data, headers=headers)
    plugin_download_url = server_response.json()["pluginfo"]["version"]["downloadurl"]
    download_and_extract_zip(plugin_download_url, full_plugin_path)
    print_ok(f'Plugin {plugin} downloaded')

# =================== Kernänderungen ===================
print_divider("Applying corechanges")
corechanges_folder_list = get_files_in_folder("corechanges")
dict_pairs = create_dict_from_list(corechanges_folder_list)

for key in dict_pairs:
    key_path = os.path.join("corechanges", str(key))
    value_path = os.path.join("corechanges", str(dict_pairs[key]))

    moodle_path_str = str(filename_to_path(dict_pairs[key]))
    moodle_path = os.path.join("moodle", moodle_path_str)

    checksum_key = hashlib.sha256(open(key_path, "rb").read()).hexdigest()
    checksum_moodle = hashlib.sha256(open(moodle_path, "rb").read()).hexdigest()
    # copy file from default to another path
    plugin_name = os.path.basename(filename_to_path(value_path))
    if checksum_key == checksum_moodle:
        # shutil.copy(value_path, moodle_path)
        print_ok(f'Applied corechange: {plugin_name}')
        # print(f"Copied {value_path} to {moodle_path}")
    else:
        print_fail(f'Original file {plugin_name} has changed. Skipping Plugin.')
