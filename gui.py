import burnaddress
import Tkinter

class App(Tkinter.Frame):
    def __init__(self, *args, **kwargs):
        Tkinter.Frame.__init__(self, *args, **kwargs)
        self.create_widgets()

    def create_widgets(self):
        warning = 'WARNING: THESE ADDRESSES ARE UNSPENDABLE!!'
        self.warning_a = Tkinter.Label(self, text=warning, bg='red')
        self.warning_a.grid(row=0, column=0, columnspan=4)

        self.vanity_label = Tkinter.Label(self, text='Vanity String (base58):')
        self.vanity_label.grid(row=1, column=0)

        self.vanity_var   = Tkinter.StringVar(self)
        self.vanity_entry = Tkinter.Entry(self, textvariable=self.vanity_var)
        self.vanity_entry.grid(row=1, column=1, columnspan=3)
        self.vanity_entry.bind('<Return>', self.process_from_vanity)

        self.bytes_label = Tkinter.Label(self, text='Bytes (hex):')
        self.bytes_label.grid(row=3, column=0)

        self.version_label = Tkinter.Label(self, text='Version:')
        self.version_label.grid(row=2, column=1)

        self.version_var   = Tkinter.StringVar(self)
        self.version_entry = Tkinter.Entry(self, textvariable=self.version_var,
                                           width=2)
        self.version_entry.grid(row=3, column=1)
        self.version_entry.bind('<Return>', self.process_from_payload)

        self.payload_label = Tkinter.Label(self, text='Payload:')
        self.payload_label.grid(row=2, column=2)

        self.payload_var   = Tkinter.StringVar(self)
        self.payload_entry = Tkinter.Entry(self, textvariable=self.payload_var,
                                           width=2*20)
        self.payload_entry.grid(row=3, column=2)
        self.payload_entry.bind('<Return>', self.process_from_payload)

        self.checksum_label = Tkinter.Label(self, text='Checksum:')
        self.checksum_label.grid(row=2, column=3)

        self.checksum_var   = Tkinter.StringVar(self)
        self.checksum_entry = Tkinter.Entry(self, textvariable=self.checksum_var,
                                           width=2*4)
        self.checksum_entry.grid(row=3, column=3)
        self.checksum_entry.bind('<Return>', self.process_from_checksum)

        self.address_label = Tkinter.Label(self, text='Address (base58):')
        self.address_label.grid(row=4, column=0)

        self.address_var   = Tkinter.StringVar(self)
        self.address_entry = Tkinter.Entry(self, textvariable=self.address_var,
                                           width=40)
        self.address_entry.grid(row=4, column=1, columnspan=3)

        self.warning_b = Tkinter.Label(self, text=warning, bg='red')
        self.warning_b.grid(row=5, column=0, columnspan=4)

    def process_from_payload(self, event=None):
        self.version_and_payload_to_checksum()
        self.bytes_to_address()

    def process_from_checksum(self, event=None):
        self.bytes_to_address()

    def process_from_vanity(self, event=None):
        vanity = self.vanity_var.get()
        base58check = burnaddress.base58_to_base58check(vanity)
        version, payload = burnaddress.decode_base_58_check(base58check)
        self.version_var.set(version.encode('hex'))
        self.payload_var.set(payload.encode('hex'))
        self.version_and_payload_to_checksum()
        self.bytes_to_address()

    def version_and_payload_to_checksum(self):
        bytes = (self.version_var.get() + self.payload_var.get()).decode('hex')
        checksum = burnaddress.checksum(bytes)
        self.checksum_var.set(checksum.encode('hex'))
        

    def bytes_to_address(self):
        bytes = (self.version_var.get() + self.payload_var.get() + self.checksum_var.get()).decode('hex')
        base58 = burnaddress.encode_base_58(bytes)
        self.address_var.set(base58)


def main():
    rt = Tkinter.Tk()
    app = App(rt)
    app.grid()
    app.mainloop()

if __name__ == '__main__':
    main()
