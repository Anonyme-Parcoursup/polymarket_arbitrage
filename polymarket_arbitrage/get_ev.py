from math import floor

BANKROLL = 000000 

def bet_price_accu(ammount, poly_price, max_size):
    size = round(ammount / poly_price, 0)
    max_size = round(max_size / poly_price, 2)
    if size > max_size:
        size = floor(max_size)
    if size == 0:
        size = 1
    return(round(size * poly_price, 2))

def bet_price(odd, p, poly_price, max_size):
    q = 1 - p
    odd = odd - 1
    if odd == 0:
        odd = 0.0001
    bet_porcent = ((odd * p) - q) / odd
    mise = bet_price_accu((bet_porcent * BANKROLL) * 0.075, poly_price, max_size)
    if mise == 0:
        mise = -0.0001
    return mise
def get_ev(w_dom, w_draw, w_ext, p_dom, p_draw, p_ext, p_no_dom, p_no_draw, p_no_ext, dom, ext, dom_size, draw_size, ext_size, no_dom_size, no_draw_size, no_ext_size):
    data = []
    w_dom = round(w_dom, 2)
    w_draw = round(w_draw, 2)
    w_ext = round(w_ext, 2)
    dom_size = round(dom_size * (p_dom / 100), 2)
    draw_size = round(draw_size * (p_draw / 100), 2)
    ext_size = round(ext_size * (p_ext / 100), 2)
    no_dom_size = round(no_dom_size * (p_no_dom / 100), 2)
    no_draw_size = round(no_draw_size * (p_no_draw / 100), 2)
    no_ext_size = round(no_ext_size * (p_no_ext / 100), 2)
    mise_dom = bet_price(1 / (p_dom / 100),(w_dom / 100), p_dom / 100, dom_size)
    mise_draw = bet_price(1 / (p_draw / 100),(w_draw / 100), p_draw / 100, draw_size)
    mise_ext = bet_price(1 / (p_ext / 100),(w_ext / 100), p_ext / 100, ext_size)
    mise_no_dom = bet_price(1 / (p_no_dom / 100), (1 - (w_dom / 100)), p_no_dom / 100, no_dom_size)
    mise_no_draw = bet_price(1 / (p_no_draw / 100), (1 - (w_draw / 100)), p_no_draw / 100, no_draw_size)
    mise_no_ext = bet_price(1 / (p_no_ext / 100), (1 - (w_ext / 100)), p_no_ext / 100, no_ext_size)
    EV_dom = round((((w_dom / 100) * (((1 / (p_dom / 100)) * 1) - 1)) - (1 * (1 - (w_dom / 100)))) * 100, 2)
    EV_draw = round((((w_draw / 100) * (((1 / (p_draw / 100)) * 1) - 1)) - (1 * (1 - (w_draw / 100)))) * 100, 2)
    EV_ext = round((((w_ext / 100) * (((1 / (p_ext / 100)) * 1) - 1)) - (1 * (1 - (w_ext / 100)))) * 100, 2)
    EV_no_dom = round((((1 - (w_dom / 100)) * ((1 / (p_no_dom / 100)) - 1) * 1) + (((w_dom / 100)) * -1))* 100, 2)
    EV_no_draw = round((((1 - (w_draw / 100)) * ((1 / (p_no_draw / 100)) - 1) * 1) + (((w_draw / 100)) * -1)) * 100, 2)
    EV_no_ext = round((((1 - (w_ext / 100)) * ((1 / (p_no_ext / 100)) - 1) * 1) + (((w_ext / 100)) * -1)) * 100, 2)
    if EV_dom > 10 and abs(w_dom - p_dom) > 8:
        EV_dom = round(((w_dom / 100) * (1 / (p_dom / 100) * mise_dom - mise_dom)) - ((1 - w_dom / 100) * mise_dom), 2)
        if dom_size < mise_dom :
            mise_dom = bet_price_accu(mise_dom, (p_dom) / 100, dom_size)
            EV_dom = round(((w_dom / 100) * (1 / (p_dom / 100) * mise_dom - mise_dom)) - ((1 - w_dom / 100) * mise_dom), 2)
        data.append([f"YES {dom}", w_dom, p_dom, EV_dom, mise_dom, dom_size, "yes_dom"])
    if EV_draw > 10 and abs(w_draw - p_draw) > 8:
        EV_draw = round(((w_draw / 100) * (1 / (p_draw / 100) * mise_draw - mise_draw)) - ((1 - w_draw / 100) * mise_draw), 2)
        if draw_size < mise_draw :
            mise_draw = bet_price_accu(mise_draw, (p_draw) / 100, draw_size)
            EV_draw = round(((w_draw / 100) * (1 / (p_draw / 100) * mise_draw - mise_draw)) - ((1 - w_draw / 100) * mise_draw), 2)    
        data.append([f"YES DRAW ({dom})", w_draw, p_draw, EV_draw, mise_draw, draw_size, "yes_draw"])        
    if EV_ext > 10 and abs(w_ext - p_ext) > 8:
        EV_ext = round(((w_ext / 100) * (1 / (p_ext / 100) * mise_ext - mise_ext)) - ((1 - w_ext / 100) * mise_ext), 2)
        if ext_size < mise_ext :
            mise_ext = bet_price_accu(mise_ext, (p_ext) / 100, ext_size)
            EV_ext = round(((w_ext / 100) * (1 / (p_ext / 100) * mise_ext - mise_ext)) - ((1 - w_ext / 100) * mise_ext), 2)  
        data.append([f"YES {ext}", w_ext, p_ext, EV_ext, mise_ext, ext_size, "yes_ext"])          
    if EV_no_dom > 10 and abs(100 - w_dom - p_no_dom) > 8:
        EV_no_dom = round(((1 - (w_dom / 100)) * (1 / (p_no_dom / 100) * mise_no_dom - mise_no_dom)) - ((w_dom / 100) * mise_no_dom), 2)
        if no_dom_size < mise_no_dom :
            mise_no_dom = bet_price_accu(mise_no_dom, (p_no_dom) / 100, no_dom_size)
            EV_no_dom = round((((100 - w_dom) / 100) * (1 / (p_no_dom / 100) * mise_no_dom - mise_no_dom)) - ((1 - (100 - w_dom) / 100) * mise_no_dom), 2)     
        data.append([f"NO {dom}", 100 - w_dom, p_no_dom, EV_no_dom, mise_no_dom, no_dom_size, "no_dom"])       
    if EV_no_draw > 10 and abs(100 - w_draw - p_no_draw) > 8:
        EV_no_draw = round(((1 - (w_draw / 100)) * (1 / (p_no_draw / 100) * mise_no_draw - mise_no_draw)) - ((w_draw / 100) * mise_no_draw), 2)
        if no_draw_size < mise_no_draw :
            mise_no_draw = bet_price_accu(mise_no_draw, (p_no_draw) / 100, no_draw_size)
            EV_no_draw = round((((100 - w_draw) / 100) * (1 / (p_no_draw / 100) * mise_no_draw - mise_no_draw)) - ((1 - (100 - w_draw) / 100) * mise_no_draw), 2)      
        data.append([f"NO DRAW ({dom})", 100 - w_draw, p_no_draw, EV_no_draw, mise_no_draw, no_draw_size, "no_draw"])        
    if EV_no_ext > 10 and abs(100 - w_ext - p_no_ext) > 8:
        EV_no_ext = round(((1 - (w_ext / 100))*(1 / (p_no_ext / 100) * mise_no_ext - mise_no_ext)) - ((w_ext / 100) * mise_no_ext), 2)
        if no_ext_size < mise_no_ext :
            mise_no_ext = bet_price_accu(mise_no_ext, (p_no_ext) / 100, no_ext_size)
            EV_no_ext = round((((100 - w_ext) / 100) * (1 / (p_no_ext / 100) * mise_no_ext - mise_no_ext)) - ((1 - (100 - w_ext) / 100) * mise_no_ext), 2)   
        data.append([f"NO {ext}", 100 - w_ext, p_no_ext, EV_no_ext, mise_no_ext, no_ext_size, "no_ext"])           
    return data