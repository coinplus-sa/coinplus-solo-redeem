"""GUI using QT to regenereate private key from the secrets engraved on COINPLUS SOLO"""
import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QGroupBox, QPushButton, QGridLayout, QLabel,\
                            QLineEdit, QRadioButton, QHBoxLayout, QVBoxLayout, QMainWindow, QScrollArea, QMessageBox

from coinplus_solo_redeem.common import compute_privatekey_sec256k1, compute_public_key_sec256k1, wif_export_bitcoin,\
    address_from_publickey_bitcoin, wif_export_litecoin, address_from_publickey_litecoin, address_from_publickey_etherum, address_from_publickey_ripple,\
    verify_address, is_b58_string
from coinplus_solo_redeem.pro import secret1_reconstruct_base58, secret2_reconstruct_base58

def resource_path(relative):
    """pyinstaller function for windows"""
    return os.path.join(
        os.environ.get(
            "_MEIPASS2",
            os.path.abspath(".")
        ),
        relative
    )

class SoloApp(QMainWindow):
    """main solo app"""
    def __init__(self):
        super(SoloApp, self).__init__()
        self.title = 'COINPLUS SOLO'
        self.setWindowTitle(self.title)
        self.setCentralWidget(SoloChoice(self))
        self.show()

class InputLabel(QWidget):
    """input with label using Horizontal box"""
    def __init__(self, label_txt="", default=""):
        super(InputLabel, self).__init__()
        self.hbox = QHBoxLayout()
        self.setLayout(self.hbox)
        self.label = QLabel(label_txt)
        self.edit = QLineEdit(default)

        self.hbox.addWidget(self.label)
        self.hbox.addWidget(self.edit)
        self.textChanged = self.edit.textChanged #pylint: disable=invalid-name

        self.text = self.edit.text
        self.setEnabled = self.edit.setEnabled #pylint: disable=invalid-name
        self.setText = self.edit.setText #pylint: disable=invalid-name
        self.setMaxLength = self.edit.setMaxLength #pylint: disable=invalid-name

class SoloChoice(QWidget):
    """Main widget"""
    def set_currency(self, currency):
        """set the currency for the app and check input"""
        self.currency = currency
        self.validate_input()

    def set_type(self, solo_type):
        """set the type for the app and check input"""
        self.solo_type = solo_type
        self.display_secret_form()
        self.validate_input()

    def __init__(self, parent):
        self.currency = "BTC"
        self.solo_type = "SOLO"

        super(SoloChoice, self).__init__(parent)
        self.setMinimumHeight(500)
        self.setMinimumWidth(460)
        self.vbox = QVBoxLayout()
        self.setLayout(self.vbox)

        self.currency_box = QGroupBox()
        self.currency_box.setTitle('Currency')
        self.currency_layout = QGridLayout()
        self.currency_box.setLayout(self.currency_layout)

        self.currency_btc = QRadioButton("Bitcoin")
        self.currency_btc.setChecked(True)
        self.currency_btc.toggled.connect(lambda: self.set_currency("BTC"))
        self.currency_eth = QRadioButton("Ether")
        self.currency_eth.toggled.connect(lambda: self.set_currency("ETH"))
        self.currency_ltc = QRadioButton("Litecoin")
        self.currency_ltc.toggled.connect(lambda: self.set_currency("LTC"))
        self.currency_xrp = QRadioButton("Ripple")
        self.currency_xrp.toggled.connect(lambda: self.set_currency("XRP"))

        self.currency_layout.addWidget(self.currency_btc, 0, 0)
        self.currency_layout.addWidget(self.currency_eth, 1, 0)
        self.currency_layout.addWidget(self.currency_ltc, 0, 1)
        self.currency_layout.addWidget(self.currency_xrp, 1, 1)

        self.is_solo = QRadioButton("SOLO")
        self.is_solo_pro = QRadioButton("SOLO PRO")
        self.is_solo.setChecked(True)
        self.is_solo.toggled.connect(lambda: self.set_type("SOLO"))
        self.is_solo_pro.toggled.connect(lambda: self.set_type("SOLO PRO"))

        self.vbox.addWidget(self.currency_box)

        self.type_box = QGroupBox()
        self.type_box.setTitle('Type')
        self.vbox.addWidget(self.type_box)
        self.network_layout = QGridLayout()
        self.type_box.setLayout(self.network_layout)
        self.network_layout.addWidget(self.is_solo, 0, 0)
        self.network_layout.addWidget(self.is_solo_pro, 0, 1)

        self.address = InputLabel('Address')
        self.address.textChanged.connect(self.validate_input)
        self.vbox.addWidget(self.address)
        self.page4f = QGroupBox()
        self.page4f.setTitle('Secrets')
        self.vbox.addWidget(self.page4f)
        self.vbox.addStretch()

        self.page4 = QVBoxLayout()

        self.solo_solo_pro = QVBoxLayout()
        self.page4f.setLayout(self.solo_solo_pro)
        self.vbox.addStretch()

        self.button_retrieve = QPushButton("Recompute private key!")
        self.button_retrieve.setEnabled(False)
        self.button_retrieve.clicked.connect(self.button_clicked_retrievepk)
        self.vbox.addWidget(self.button_retrieve)

        self.solo_widget = SoloWidget(self.validate_input)
        self.solo_pro_widget = SoloProWidget(self.validate_input)
        self.solo_solo_pro.addWidget(self.solo_widget)
        self.solo_solo_pro.addWidget(self.solo_pro_widget)

        self.display_secret_form()

    def display_secret_form(self):
        """display SOLO widget or SOLO Pro widget depending on the type of solo"""
        self.solo_widget.hide()
        self.solo_pro_widget.hide()
        if self.solo_type == "SOLO":
            self.solo = self.solo_widget
            self.solo_widget.show()
        if self.solo_type == "SOLO PRO":
            self.solo_pro_widget.show()
            self.solo = self.solo_pro_widget

    def validate_input(self):
        """verifiy the input and enable or disable the button"""
        state = True
        if self.solo.validate() is False:
            state = False
        if verify_address(self.address.text(), self.currency) is False:
            state = False
        self.button_retrieve.setEnabled(state)

    def button_clicked_retrievepk(self):
        """button action function to recompute the private key"""
        secret1_b58, secret2_b58 = self.solo.get_secrets()

        privkey256 = compute_privatekey_sec256k1(secret1_b58, secret2_b58)
        public_key = compute_public_key_sec256k1(privkey256)
        if self.currency == "BTC":
            privatekey_wif = wif_export_bitcoin(privkey256)
            address = address_from_publickey_bitcoin(public_key)
        if self.currency == "LTC":
            privatekey_wif = wif_export_litecoin(privkey256)
            address = address_from_publickey_litecoin(public_key)
        if self.currency == "ETH":
            privatekey_wif = privkey256.hex()
            public_key_un = compute_public_key_sec256k1(privkey256, compressed=False)
            address = address_from_publickey_etherum(public_key_un)
        if self.currency == "XRP":
            privatekey_wif = privkey256.hex()
            address = address_from_publickey_ripple(public_key)
        if self.address.text() != address:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error, the secret key do not correspond to the address you entered, ")
            msg.setInformativeText("please check that you entered the secrets correctly")
            msg.setWindowTitle("Error during key recomputation")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
        else:
            msg = QMessageBox()
#            msg.setIconPixmap(QPixmap(resource_path("img/success.png")));
            msg.setText("Success! The computation of your private key was successful:")
            msg.setInformativeText(privatekey_wif)
            msg.setWindowTitle("Success")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

class SoloProWidget(QWidget):
    """Widget for the Solo Pro"""
    def __init__(self, textchanged):
        super(SoloProWidget, self).__init__()
        self.vbox_window = QVBoxLayout()
        self.setLayout(self.vbox_window)

        self.require = InputLabel("Required number of secrets : ", "2")
        self.require.textChanged.connect(self.on_required_change)
        self.vbox_window.addWidget(self.require)

        self.box_recover = QGroupBox()
        self.box_recover.setTitle('SOLO PRO')
        self.vbox_window.addWidget(self.box_recover)

        self.secrets_recover = None

        self.vbox_recover = QVBoxLayout()

        self.box_recover.setLayout(self.vbox_recover)
        self.textchanged = textchanged

        self.secrets_recover = QScrollArea()
        self.scroll_area_widget_contents2 = QWidget()
        self.secrets_recover.setWidget(self.scroll_area_widget_contents2)
        self.secrets_recover.setWidgetResizable(True)
        self.vbox_recover_secrets = QVBoxLayout()
        self.scroll_area_widget_contents2.setLayout(self.vbox_recover_secrets)

        self.vbox_recover.addWidget(self.secrets_recover)

        self.secrets_recover_list = []
        self.vbox_window.addWidget(self.box_recover)

        self.on_required_change()

    def validate(self):
        """check if the parameters are valid"""
        for secret in self.secrets_recover_list:
            sec, _ = secret.get_secret(1)
            if not is_b58_string(sec, size=28):
                return False
            sec, _ = secret.get_secret(2)
            if not is_b58_string(sec, size=14):
                return False
        return True

    def get_secrets(self):
        """recompute the secret 1 and secret 2 from the shamir shares and return the 2 solo secrets"""
        shares1 = []
        shares2 = []
        for secret in self.secrets_recover_list:
            sec, numi = secret.get_secret(1)
            shares1.append((int(numi), sec))
            sec, numi = secret.get_secret(2)
            shares2.append((int(numi), sec))
        s1 = secret1_reconstruct_base58(shares1)
        s2 = secret2_reconstruct_base58(shares2)
        return s1, s2

    def on_required_change(self):
        """Automatically adapt the layout depending on the number of required secrets"""
        for i in range(len(self.secrets_recover_list)):
            self.vbox_recover_secrets.removeWidget(self.secrets_recover_list[i])
            self.secrets_recover_list[i].deleteLater()

        number_required = 0
        try:
            number_required = int(self.require.text())

        except  ValueError:
            pass

        self.secrets_recover_list = []
        for i in range(0, number_required):
            secretWidget = SoloProSecret(self)
            self.secrets_recover_list.append(secretWidget)
        for i in range(len(self.secrets_recover_list)):
            self.vbox_recover_secrets.addWidget(self.secrets_recover_list[i])

class SoloProSecret(QGroupBox):
    """Widget for the Solo """
    def __init__(self, parent):
        super(SoloProSecret, self).__init__(parent=parent)
        self.setTitle('Secret')
        self.secret_vlayout = QVBoxLayout(self)

        self.pro_num = InputLabel("Solo Pro number (#):")
        self.secret1 = InputLabel("Secret 1:")
        self.secret2 = InputLabel("Secret 2:")
        self.secret1.setMaxLength(28)
        self.secret2.setMaxLength(14)
        self.pro_num.textChanged.connect(parent.textchanged)
        self.secret1.textChanged.connect(parent.textchanged)
        self.secret2.textChanged.connect(parent.textchanged)

        self.secret_vlayout.addWidget(self.pro_num)
        self.secret_vlayout.addWidget(self.secret1)
        self.secret_vlayout.addWidget(self.secret2)

    def get_secret(self, number):
        """retrieve the secret from the widget"""
        if number == 1:
            sec, num = self.secret1.text(), self.pro_num.text()
        elif number == 2:
            sec, num = self.secret2.text(), self.pro_num.text()
        else:
            raise Exception("wrong secret number")
        return sec, num

class SoloWidget(QWidget):
    """Solo widget"""
    def __init__(self, textchanged):
        """initialize the SoloWidget with the callback when text is modified"""
        super(SoloWidget, self).__init__()
        self.vbox = QVBoxLayout()
        self.setLayout(self.vbox)

        self.secret1 = InputLabel('Secret 1:')
        self.secret1.textChanged.connect(textchanged)
        self.vbox.addWidget(self.secret1)

        self.secret2 = InputLabel('Secret 2:')
        self.secret2.textChanged.connect(textchanged)
        self.vbox.addWidget(self.secret2)
        self.secret1.setMaxLength(28)
        self.secret2.setMaxLength(14)

    def validate(self):
        """return the inputs from the widget"""
        sec = self.secret1.text()
        if not is_b58_string(sec, size=28):
            return False
        sec = self.secret2.text()
        if not is_b58_string(sec, size=14):
            return False
        return True
    def get_secrets(self):
        """return the secrets from the widget"""
        return self.secret1.text(), self.secret2.text()

def main():
    """Main function callable from setup script"""
    app = QApplication(sys.argv)
    ex = SoloApp() #pylint: disable=unused-variable
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
