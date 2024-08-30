# small gui app to display basic network information give an IP Address and a
# CIDR Prefix or Subnetmask. Uses the ipaddress library. The submodule network.py
# can be used standalone from the cli
import network as net
import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as ttk
import ipaddress
import base64
from io import BytesIO
from PIL import Image, ImageTk

class App(ttk.Window):
    """Main Window"""
    def __init__(self):
        super().__init__(themename='darkly')
        self.title('Network Tool')
        self.geometry('300x350')
        self.resizable(False, False)

        self.entry_ip = Entry(self, '0', 'normal', 'Ip-Adress', entry_cidr=True)
        self.entry_sub = Entry(self, '0', 'readonly', 'Subnetmask')
        self.radio_buttons = Toggle(self, self.entry_sub, self.entry_ip)

        self.button_submit = ttk.Button(self, text='Submit', command=self.show_network, takefocus=False)
        self.button_submit.pack(pady=(10, 10))

        self.result_frame = FrameResult(self)
        self.result_frame.pack(expand=True, fill='x', padx=20)

        self.entry_ip.cidr_field.bind('<Return>', self.update_subnetmask)

        self.mainloop()

    def show_network(self):
        """Display the network information in the Main Window. Check if mask and ip
        are valid"""
        ip = self.validate_ip()
        subnetmask = self.get_mask()
        try:
            network = ipaddress.ip_network((ip + '/' + subnetmask), strict=False)
            self.result_frame.update_labels(
                network_id=network.network_address,
                first_host=net.first_host_get(network),
                last_host=net.last_host_get(network),
                broadcast=network.broadcast_address,
                max_hosts=network.num_addresses - 2
            )
            self.update_subnetmask(subnetmask.split('.'))
        except ValueError as e:
            messagebox.showerror(title='Invalid Network', message=f'Something went wrong. Check IP and Subnetmask. Error: {e}')


    def validate_ip(self):
        """Get the ip from the Entries and check if its valid. If not show a
        warning and reset ip to 0.0.0.0"""
        ip_lst = self.entry_ip.get_values()
        ip = f"{ip_lst[0]}.{ip_lst[1]}.{ip_lst[2]}.{ip_lst[3]}"
        try:
            net.ipaddress.ip_address(ip)
        except:
            messagebox.showwarning(title='Invalid IP', message='Invalid IP-Address. Please enter a valid IP')
            ip = '0.0.0.0'
            for octet in self.entry_ip.octet_list:
                octet.delete(0, tk.END)
                octet.insert(0,'0')
        return ip

    def get_mask(self):
        """Check which input we use for the subnetmask (prefix or subnetmask). Get
        the the subnetmask and return it if it is valid"""
        if not self.entry_ip.cidr_field.instate(['readonly']):
            cidr_value = self.entry_ip.get_cidr_value()
            subnetmask = net.cidr_to_sub(cidr_value)
        else:
            sub_lst = self.entry_sub.get_values()
            subnetmask = f'{sub_lst[0]}.{sub_lst[1]}.{sub_lst[2]}.{sub_lst[3]}'
            if subnetmask not in net.cidr_to_subnet.values():
                messagebox.showwarning(title='Invalid Mask', message='Invalid Subnetmask. Please enter a valid mask')
                subnetmask = '0.0.0.0'
                for octet in self.entry_sub.octet_list:
                    octet.delete(0, tk.END)
                    octet.insert(0,'0')
        return subnetmask

    def update_subnetmask(self, subnetmask):
        """If we get the mask by the prefix, we insert the values into the
        subnetmask entries"""
        if self.entry_sub.octet_list[0].instate(['readonly']):
            self.entry_sub.toggle_state('normal')
            counter = 0
            for octet in self.entry_sub.octet_list:
                octet.delete(0, tk.END)
                octet.insert(0,subnetmask[counter])
                counter += 1
            self.entry_sub.toggle_state('readonly')

class Toggle(ttk.Frame):
    """Toggling what information we use: subnetmask or prefix and setting the not
    used to readonly"""
    def __init__(self, parent, entry_sub, entry_ip):
        super().__init__(parent)
        self.pack()
        self.radio = tk.StringVar(value='cidr')

        self.entry_sub = entry_sub
        self.entry_ip = entry_ip

        self.radio_sub = ttk.Radiobutton(
            self, 
            text='Use Subnetmask', 
            value='sub', 
            variable=self.radio, 
            command=self.toggle_entries)
        self.radio_cidr = ttk.Radiobutton(
            self, 
            text='Use CIDR Prefix', 
            value='cidr', 
            variable=self.radio, 
            command=self.toggle_entries)
        
        self.radio_sub.pack(side='left', padx=(0,10), pady=10)
        self.radio_cidr.pack(side='left')

    def toggle_entries(self):
        """Funktion to toggle the state dependent on actual state"""
        if self.radio.get() == 'sub':
            self.entry_sub.toggle_state('normal')
            self.entry_ip.toggle_cidr_state('readonly')
        else:
            self.entry_sub.toggle_state('readonly')
            self.entry_ip.toggle_cidr_state('normal')
        
class Entry(ttk.Frame):
    """Creates a frame containing four entry fields sepearted by dots as input for
    an ip or subnetmask"""
    def __init__(self, parent, text, state, entry_title, entry_cidr=False):
        super().__init__(parent)
        self.pack()

        self.octet_list = []
        self.cidr_field = None
        self.entry_label = ttk.Label(self, text=entry_title, font=('Arial', 14))
        self.entry_label.pack(pady=8)

        oct_1 = Octett(self, text, state)
        ttk.Label(self, text='.').pack(side='left')
        oct_2 = Octett(self, text, state)
        ttk.Label(self, text='.').pack(side='left')
        oct_3 = Octett(self, text, state)
        ttk.Label(self, text='.').pack(side='left')
        oct_4 = Octett(self, text, state)

        # we need this list to access and manipulate the entries from within 
        # various other functions
        self.octet_list.append(oct_1)
        self.octet_list.append(oct_2)
        self.octet_list.append(oct_3)
        self.octet_list.append(oct_4)

        # create an extra field for the CIDR prefix
        if entry_cidr:
            ttk.Label(self, text='/').pack(side='left', padx=6)
            self.cidr_field = Octett(self, text, state)
            self.cidr_field.pack(side='left')

    def get_values(self):
        """Get the values from the entries as a list"""
        return [octet.get_value() for octet in self.octet_list]
    
    def get_cidr_value(self):
        """Get the Prefix from the extra entry"""
        if self.cidr_field:
            return self.cidr_field.get_value()
        return None
    
    def toggle_state(self, new_state):
        """toggle the state of all entries"""
        for octet in self.octet_list:
            octet.config(state=new_state)

    def toggle_cidr_state(self, new_state):
        """toggle the state of the cidr entry"""
        if self.cidr_field:
            self.cidr_field.config(state=new_state)

class Octett(ttk.Entry):
    """Create single Entry Field with focus in and focus out bindings"""
    def __init__(self, parent, text, state):
        super().__init__(
            parent, 
            justify='center', 
            width='5', 
            foreground='lightgrey', 
            state=state)
        
        self.pack(side='left')
        self.insert(0,text)

        def entry_focus_in(event):
            """empty the field if it gets focus"""
            if event.widget.get() != '':
                event.widget.delete(0, tk.END)

        def entry_focus_out(event):
            """insert 0 if entry looses focus without input"""
            if event.widget.get() == '':
                event.widget.insert(0, '0')

        self.bind('<FocusIn>', entry_focus_in)
        self.bind('<FocusOut>', entry_focus_out)

    def get_value(self):
        """return entry value"""
        return self.get()
    
class FrameResult(ttk.Frame):
    """create a Frame with two columns listing all the relevant network information"""
    def __init__(self, parent):
        super().__init__(parent)

        image_data = b'iVBORw0KGgoAAAANSUhEUgAAABIAAAASCAYAAABWzo5XAAAACXBIWXMAAAsSAAALEgHS3X78AAAA8klEQVQ4ja3UO04DMRSF4c+ZPCiQ2AMpYEmAxN5QKhZAHyrWQAHLAERCMhTjS0aRPSJRTmPLPv597/UjtW3rFBrndoobXGGNVPFvcIEnLNHksT/QLR4Q4dVAq7zpRwbN8IU2QJe5Pcvm/+ozOgGKSH4wwh2uDac5xSsesQpQmLe4x8Jwmvtzi3HBNM/tLEfUFDwbTHRlmLNLrbTbtreopJhv6eqxr1pNako10FE6OahWh4NBpZM5SHFqS5wfyWj7oGe85H5EN9KlXLtHkU3qgxq7C/aWx777xlIUWe+Qev9RyoaJ7ksZemvhi7e2Tqf62H4B9YE61b9mQxkAAAAASUVORK5CYII='
        self.pil_image = Image.open(BytesIO(base64.b64decode(image_data)))
        self.image = ImageTk.PhotoImage(self.pil_image)

        self.rowconfigure((1,2,3,4,5), weight=1, uniform='a')
        self.columnconfigure(1, weight=1, uniform='a')
        self.columnconfigure(2, weight=4, uniform='a')

        self.Label_netid = ttk.Label(self, text='Network Adress: ', font=('Arial', 10))
        self.Label_first_host = ttk.Label(self, text='First Host IP: ', font=('Arial', 10))
        self.Label_last_host = ttk.Label(self, text='Last Host IP: ', font=('Arial', 10))
        self.Label_broadcast = ttk.Label(self, text='Broadcast Adress: ', font=('Arial', 10))
        self.Label_max_hosts = ttk.Label(self, text='Max. # of Hosts: ', font=('Arial', 10))

        self.Label_netid.grid(row=0, column=0, sticky='e')
        self.Label_first_host.grid(row=1, column=0, sticky='e')
        self.Label_last_host.grid(row=2, column=0, sticky='e')
        self.Label_broadcast.grid(row=3, column=0, sticky='e')
        self.Label_max_hosts.grid(row=4, column=0, sticky='e')

        
        self.Label_netid_result = ttk.Label(self, text='0.0.0.0', font=('Arial', 10))
        self.Label_first_host_result = ttk.Label(self, text='0.0.0.1', font=('Arial', 10))
        self.Label_last_host_result = ttk.Label(self, text='255.255.255.254', font=('Arial', 10))
        self.Label_broadcast_result = ttk.Label(self, text='255.255.255.255', font=('Arial', 10))
        self.Label_max_hosts_result = ttk.Label(self, text='4294967294', font=('Arial', 10))

        self.Label_netid_result.grid(row=0, column=1, columnspan=3, sticky='w')
        self.Label_first_host_result.grid(row=1, column=1, columnspan=3, sticky='w')
        self.Label_last_host_result.grid(row=2, column=1, columnspan=3, sticky='w')
        self.Label_broadcast_result.grid(row=3, column=1, columnspan=3, sticky='w')
        self.Label_max_hosts_result.grid(row=4, column=1, columnspan=3, sticky='w')

        self.button_netid = tk.Button(
            self, 
            text='Copy', 
            image=self.image, 
            command=lambda: self.copy_to_clipboard(self.Label_netid_result.cget('text')))
        self.button_first_host = tk.Button(
            self, 
            text='Copy', 
            image=self.image, 
            command=lambda: self.copy_to_clipboard(self.Label_first_host_result.cget('text')))
        self.button_last_host = tk.Button(
            self, 
            text='Copy', 
            image=self.image, 
            command=lambda: self.copy_to_clipboard(self.Label_last_host_result.cget('text')))
        self.button_broadcast = tk.Button(
            self, 
            text='Copy', 
            image=self.image, 
            command=lambda: self.copy_to_clipboard(self.Label_broadcast_result.cget('text')))
        self.button_max_hosts = tk.Button(
            self, 
            text='Copy', 
            image=self.image, 
            command=lambda: self.copy_to_clipboard(self.Label_max_hosts_result.cget('text')))

        self.button_netid.grid(row=0, column=4, sticky='e', ipady=1, ipadx=1)
        self.button_first_host.grid(row=1, column=4, sticky='e', ipady=1, ipadx=1)
        self.button_last_host.grid(row=2, column=4, sticky='e', ipady=1, ipadx=1)
        self.button_broadcast.grid(row=3, column=4, sticky='e', ipady=1, ipadx=1)
        self.button_max_hosts.grid(row=4, column=4, sticky='e', ipady=1, ipadx=1)

    def update_labels(self, network_id, first_host, last_host, broadcast, max_hosts):
        """update the Labels"""
        self.Label_netid_result.config(text=network_id)
        self.Label_first_host_result.config(text=first_host)
        self.Label_last_host_result.config(text=last_host)
        self.Label_broadcast_result.config(text=broadcast)
        self.Label_max_hosts_result.config(text=max_hosts)

    def copy_to_clipboard(self, label):
        """copy the content of the corresponding result label to the clipboard"""
        self.clipboard_clear()
        self.clipboard_append(label)
        self.update()

# run
App()