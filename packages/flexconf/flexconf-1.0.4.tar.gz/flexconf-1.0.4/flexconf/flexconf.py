import inspect
import os
from argparse import ArgumentParser, Namespace
from configparser import ConfigParser
from pathlib import Path

#  __init__で--debug, --patternを追加するだけのデフォルトパーサ
default_parser = ArgumentParser()


class FlexConf:
    """Flexible Configuration

    コマンドライン引数によって読み込み先の設定を変更できる

    Example
    -------
    以下のように、ライブラリを使用するスクリプトと同じ階層に`.flexconf`ディレクトリを作成する
    ```sh
    .
    ├─ .flexconf/
    │   ├─ pattern1.conf
    │   └─ pattern2.conf
    └─ sample.py         # ライブラリを使用するスクリプト
    ```

    それぞれの設定ファイルは以下のような構成にする
    ```conf
    # pattern1.conf
    [DEFAULT]           # 必ず書く
    A = 3               # パラメータ名 = 値 という書式で記述する
    B = 1920 1080       # 値にものが文字列として読み込まれる
    ```

    この設定を利用するサンプルプログラム
    ```py
    # sample.py
    from flexconf import FlexConf

    class SubClass(FlexConf):
        # __init__を定義する必要はない
        # 定義する場合は、super().__init__()を実行する
        def __init__(self):
            # do something here
            super().__init__()

        def sample_method(self):
            # `./.flexconf/*.conf`に定義したパラメータの値を
            # self.パラメータ名 で取得することができる
            print(self.A)
            print(self.B)

    if __name__ == "__main__":
        s = SubClass()
        s.sample_method()
    ```

    実行例
    ```sh
    // -p オプションで使用したい設定ファイルを選択する
    $ python sample.py -p pattern1
    3
    1920 1080
    $ python sample.py -p pattern2
    4
    hogehoge
    ```
    """

    def __init__(self, arg_parser: ArgumentParser = default_parser):
        """
        Examples
        --------
        コマンドライン引数を追加したい場合

        ```py
        parser = ArgumentParser()
        parser.add_argument(
            "arg1",
            help="first argument",
        )
        s = SubClass(parser)    # FlexConfを継承したクラスに引数で渡し、
                                # super().__init__(parser)を呼ぶ
        ```

        Parameters
        ----------
        arg_parser : ArgumentParser, optional
            コマンドライン引数を追加したパーサ, by default default_parser
        """
        # 呼び出し元（=作業ディレクトリ）の名前
        # スクリプトと同じディレクトリで実行した場合、空文字
        work_dir = os.path.dirname(inspect.stack()[1].filename)
        patterns, self.__conf_dir = generate_pattern_list(work_dir)

        # コマンドライン引数パースする
        self.comm_args: Namespace = parse_command_line(arg_parser, patterns)
        # パースした引数を適宜使いやすいように配置する
        self.is_debug_mode: bool = self.comm_args.is_debug_mode
        self.__pattern: str = self.comm_args.pattern
        # ファイルからパラメータを読み込む
        self.__load_config()

    def __load_config(self):
        """ファイルからパラメータを読み込む"""
        config = ConfigParser()
        # .confファイルに書いたパラメータ名の大文字と小文字を区別する
        config.optionxform = str
        # 読み込み
        config.read(f"{self.__conf_dir}/{self.__pattern}.conf")
        for param in config["DEFAULT"]:
            # self.パラメータ名 = パラメータ値
            exec(f'self.{param} = "{config["DEFAULT"][param]}"')


def generate_pattern_list(dir_path: str) -> set:
    """切り替え候補の設定のパターン名のリストを生成する

    Parameters
    ----------
    dir_path : str
        実行ディレクトリからの相対パス

    Returns
    -------
    set
        (パターン名のリスト、.flexconfディレクトリのパス)
    """
    path = Path(dir_path)
    # 絶対パスに変換
    dir_path = path.resolve() if not path.is_absolute() else path
    # 設定ファイルのディレクトリパス
    conf_dir = f"{dir_path}/.flexconf"
    # 設定ファイルのリスト
    conf_list = os.listdir(conf_dir)
    # それぞれの設定ファイル名のルート部をパターン名とする
    pattern_list = list(map(lambda x: os.path.splitext(x)[0], conf_list))
    return (pattern_list, conf_dir)


def parse_command_line(parser: ArgumentParser, patterns: list) -> Namespace:
    """コマンドライン引数をパースする

    Parameters
    ----------
    parser : ArgumentParser
        引数パーサ
    patterns : list
        設定パターン名のリスト

    Returns
    -------
    Namespace
        パース結果、ドット演算子でアクセスできる
    """
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        dest="is_debug_mode",
        help="show debug print",
    )
    parser.add_argument(
        "-p",
        "--pattern",
        required=True,
        choices=patterns,
        dest="pattern",
        help='Choose one of the files under the ".flexconf" directory',
    )
    # コマンドライン引数をパースする
    return parser.parse_args()


def main():
    """`python -m flexconf`で実行される関数"""
    conf_dir = "./.flexconf"
    # `.flexconf`ディレクトリを作成
    os.makedirs(conf_dir, exist_ok=True)
    template_conf = [
        "[DEFAULT]\n",
        "fruit = apple\n",
        "price = 100\n",
    ]
    # テンプレートファイルを作成
    template_path = f"{conf_dir}/template.conf"
    with open(template_path, "w") as f:
        f.writelines(template_conf)
    print("Configuration file template has been generated.")
    print(f"-> {template_path}")
