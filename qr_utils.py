import qrcode
import base64
from io import BytesIO
import json
import re


def generate_pass_qr(pass_data):
    """
    Generate QR code for a pass
    pass_data should contain: pass_number, pass_holder, mobile_no, amount_paid, issue_date, issue_time
    """
    try:
        qr_data = json.dumps({
            'pn': pass_data['pass_number'],  
            'ph': pass_data['pass_holder'][:15] if pass_data['pass_holder'] else '',  
            'mb': pass_data['mobile_no'][-4:],  
            'am': str(pass_data['amount_paid']), 
            'type': 'pass'
        }, separators=(',', ':'))  
        
        print(f"Generated QR data: {qr_data}") 
        
        qr = qrcode.QRCode(
            version=1,
            box_size=10,
            border=4,
            error_correction=qrcode.constants.ERROR_CORRECT_H  
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return f"data:image/png;base64,{img_str}"
        
    except Exception as e:
        print(f"QR generation error: {e}")
        return None


def generate_ticket_qr(ticket_data):
    """
    Generate QR code for a ticket
    ticket_data should contain: ticket_number, ticket_holder, mobile_no, amount_paid, start_dest, final_dest, issue_date, issue_time
    """
    try:
        qr_data = json.dumps({
            'tn': ticket_data['ticket_number'],  
            'th': ticket_data['ticket_holder'][:15] if ticket_data['ticket_holder'] else '',  
            'mb': ticket_data['mobile_no'][-4:],  
            'am': str(ticket_data['amount_paid']),
            'sd': ticket_data['start_dest'][:20] if ticket_data['start_dest'] else '',
            'fd': ticket_data['final_dest'][:20] if ticket_data['final_dest'] else '',
            'type': 'ticket'
        }, separators=(',', ':'))  
        
        print(f"Generated ticket QR data: {qr_data}") 
        
        qr = qrcode.QRCode(
            version=1,
            box_size=10,
            border=4,
            error_correction=qrcode.constants.ERROR_CORRECT_H  
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return f"data:image/png;base64,{img_str}"
        
    except Exception as e:
        print(f"Ticket QR generation error: {e}")
        return None


def extract_pass_number_from_qr(qr_data):
    """
    Extract just the pass number from QR data
    """
    try:
        print(f"Extracting pass number from: {qr_data[:100]}")  
        
        if qr_data.startswith('{') and qr_data.endswith('}'):
            data = json.loads(qr_data)
            pass_number = data.get('pn') or data.get('pass_number') or data.get('pass')
            if pass_number:
                return pass_number
        match = re.search(r'PS[A-Z0-9]{5}', qr_data)
        if match:
            return match.group(0)
        if re.match(r'^PS[A-Z0-9]{5}$', qr_data):
            return qr_data
            
        return None
    except Exception as e:
        print(f"QR decode error: {e}")
        return None

def extract_ticket_number_from_qr(qr_data):
    """
    Extract just the ticket number from QR data
    """
    try:
        print(f"Extracting ticket number from: {qr_data[:100]}")  
        
        if qr_data.startswith('{') and qr_data.endswith('}'):
            data = json.loads(qr_data)
            ticket_number = data.get('tn') or data.get('ticket_number') or data.get('ticket')
            if ticket_number:
                return ticket_number
        match = re.search(r'TC\d+_\d+', qr_data)
        if match:
            return match.group(0)
        if re.search(r'TC\d+', qr_data):
            return re.search(r'TC\d+', qr_data).group(0)
            
        return None
    except Exception as e:
        print(f"Ticket QR decode error: {e}")
        return None