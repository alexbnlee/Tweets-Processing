from math import radians, cos, sin, asin, sqrt
def distance(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    
    # haversine function
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6372 # ratio of earch, km
    return c * r # km

# get greater earth distance based on tuples
def get_dis(t1, t2):
    return distance(t1[0], t1[1], t2[0], t2[1])

# data processing
import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
nlp = en_core_web_sm.load()

# real lat lon
Rs = []
# lat lon from text
# _cen: centoid
Ts_cen = []
# lat lon from user location
Us_cen = []
# lat lon from place name
Ps_cen = []
# lat lon from place bounding box
Bs = []

# area of suburbs
# if getting info from bounding box, it will be setted with 0.
Areas = []

def processing_area(df_com, df_suburbs):
    Rs = []
    Ts_cen = []
    Us_cen = []
    Ps_cen = []
    Bs = []

    length = len(df_com)
    
    for i in range(length):    
        if i+1 == length:
            percent = 100.0
            print('Progress: %s [%d/%d]'%(str(percent)+'%',i+1,length),end='\n')
        else:
            percent = round(1.0 * i / length * 100,2)
            print('Progress: %s [%d/%d]'%(str(percent)+'%',i+1,length),end='\r')
        
        # real coordinates
        Rs.append((float(df_com.iloc[i]['co_lon']), float(df_com.iloc[i]['co_lat'])))
        # bounding box
        Bs.append((float(df_com.iloc[i]['pb_avg_lon']), float(df_com.iloc[i]['pb_avg_lat'])))
        
        article = df_com.iloc[i]['text_nl']
        doc = nlp(article)
        # whether appending or not
        flag_t = 0
        for X in doc.ents:
            if X.label_ in ['GPE', 'LOC']:
                res = search_suburbs(X.text, df_suburbs)
                # point in the bounding box
                if len(res) > 0 and float(res.iloc[0]['Longitude']) > float(df_com.iloc[i]['min_lon']) and \
                                    float(res.iloc[0]['Longitude']) < float(df_com.iloc[i]['max_lon']) and \
                                    float(res.iloc[0]['Latitude']) > float(df_com.iloc[i]['min_lat']) and \
                                    float(res.iloc[0]['Latitude']) < float(df_com.iloc[i]['max_lat']):
                    Ts_cen.append((float(res.iloc[0]['Longitude']), float(res.iloc[0]['Latitude'])))
                    flag_t = 1
                    break
        if not flag_t:
            Ts_cen.append(None)
            
        uloc = nlp(df_com.iloc[i]['user_location_nl'])
        flag_u = 0
        for XX in uloc.ents:
            if XX.label_ in ['GPE', 'LOC']:
                res = search_suburbs(XX.text, df_suburbs)
                if len(res) > 0 and float(res.iloc[0]['Longitude']) > float(df_com.iloc[i]['min_lon']) and \
                                    float(res.iloc[0]['Longitude']) < float(df_com.iloc[i]['max_lon']) and \
                                    float(res.iloc[0]['Latitude']) > float(df_com.iloc[i]['min_lat']) and \
                                    float(res.iloc[0]['Latitude']) < float(df_com.iloc[i]['max_lat']):
                    Us_cen.append((float(res.iloc[0]['Longitude']), float(res.iloc[0]['Latitude'])))
                    flag_u = 1
                    break    
        if not flag_u:
            Us_cen.append(None)

        place_name = nlp(df_com.iloc[i]['place_name'])
        flag_p = 0
        for X1 in place_name.ents:
            if X1.label_ in ['GPE', 'LOC']:
                res = search_suburbs(X1.text, df_suburbs)
                if len(res) > 0 and float(res.iloc[0]['Longitude']) > float(df_com.iloc[i]['min_lon']) and \
                                    float(res.iloc[0]['Longitude']) < float(df_com.iloc[i]['max_lon']) and \
                                    float(res.iloc[0]['Latitude']) > float(df_com.iloc[i]['min_lat']) and \
                                    float(res.iloc[0]['Latitude']) < float(df_com.iloc[i]['max_lat']):
                    Ps_cen.append((float(res.iloc[0]['Longitude']), float(res.iloc[0]['Latitude'])))
                    flag_p = 1
                    break
        if not flag_p:
            Ps_cen.append(None)  
    
    return Rs, Ts_cen, Us_cen, Ps_cen, Bs

# mean
def Model_TUPB_bb_cs(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim):
    Cs = []
    for i in range(len(Rs)):
        if Ts_cen[i]:
            Cs.append(Ts_cen[i])
        elif Us_cen[i]:
            Cs.append(Us_cen[i])
        elif Ps_cen[i]:
            Cs.append(Ps_cen[i])
        elif df.iloc[i]['bb_area'] >= lim:    # 如果 bounding box 面积太大，不予计算
            Cs.append((0, 0))
            continue
        else:
            Cs.append(Bs[i])
    
    dis_errs = []
    for i in range(len(Rs)):
        if Cs[i] != (0, 0):
            dis_errs.append(get_dis(Rs[i], Cs[i]))
    
    return len(dis_errs)/len(Rs), sum(dis_errs)/len(dis_errs)

def Model_TPUB_bb_cs(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim):
    Cs = []
    for i in range(len(Rs)):
        if Ts_cen[i]:
            Cs.append(Ts_cen[i])
        elif Ps_cen[i]:
            Cs.append(Ps_cen[i])
        elif Us_cen[i]:
            Cs.append(Us_cen[i])
        elif df.iloc[i]['bb_area'] >= lim:    # 如果 bounding box 面积太大，不予计算
            Cs.append((0, 0))
            continue
        else:
            Cs.append(Bs[i])
    
    dis_errs = []
    for i in range(len(Rs)):
        if Cs[i] != (0, 0):
            dis_errs.append(get_dis(Rs[i], Cs[i]))
    
    return len(dis_errs)/len(Rs), sum(dis_errs)/len(dis_errs)

def Model_UTPB_bb_cs(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim):
    Cs = []
    for i in range(len(Rs)):
        if Us_cen[i]:
            Cs.append(Us_cen[i])
        elif Ts_cen[i]:
            Cs.append(Ts_cen[i])
        elif Ps_cen[i]:
            Cs.append(Ps_cen[i])
        elif df.iloc[i]['bb_area'] >= lim:    # 如果 bounding box 面积太大，不予计算
            Cs.append((0, 0))
            continue
        else:
            Cs.append(Bs[i])
    
    dis_errs = []
    for i in range(len(Rs)):
        if Cs[i] != (0, 0):
            dis_errs.append(get_dis(Rs[i], Cs[i]))
    
    return len(dis_errs)/len(Rs), sum(dis_errs)/len(dis_errs)

def Model_UPTB_bb_cs(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim):
    Cs = []
    for i in range(len(Rs)):
        if Us_cen[i]:
            Cs.append(Us_cen[i])
        elif Ps_cen[i]:
            Cs.append(Ps_cen[i])
        elif Ts_cen[i]:
            Cs.append(Ts_cen[i])
        elif df.iloc[i]['bb_area'] >= lim:    # 如果 bounding box 面积太大，不予计算
            Cs.append((0, 0))
            continue
        else:
            Cs.append(Bs[i])
    
    dis_errs = []
    for i in range(len(Rs)):
        if Cs[i] != (0, 0):
            dis_errs.append(get_dis(Rs[i], Cs[i]))
    
    return len(dis_errs)/len(Rs), sum(dis_errs)/len(dis_errs)

def Model_PUTB_bb_cs(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim):
    Cs = []
    for i in range(len(Rs)):
        if Ps_cen[i]:
            Cs.append(Ps_cen[i])
        elif Us_cen[i]:
            Cs.append(Us_cen[i])
        elif Ts_cen[i]:
            Cs.append(Ts_cen[i])
        elif df.iloc[i]['bb_area'] >= lim:    # 如果 bounding box 面积太大，不予计算
            Cs.append((0, 0))
            continue
        else:
            Cs.append(Bs[i])
    
    dis_errs = []
    for i in range(len(Rs)):
        if Cs[i] != (0, 0):
            dis_errs.append(get_dis(Rs[i], Cs[i]))
    
    return len(dis_errs)/len(Rs), sum(dis_errs)/len(dis_errs)

def Model_PTUB_bb_cs(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim):
    Cs = []
    for i in range(len(Rs)):
        if Ps_cen[i]:
            Cs.append(Ps_cen[i])
        elif Ts_cen[i]:
            Cs.append(Ts_cen[i])
        elif Us_cen[i]:
            Cs.append(Us_cen[i])
        elif df.iloc[i]['bb_area'] >= lim:    # 如果 bounding box 面积太大，不予计算
            Cs.append((0, 0))
            continue
        else:
            Cs.append(Bs[i])
    
    dis_errs = []
    for i in range(len(Rs)):
        if Cs[i] != (0, 0):
            dis_errs.append(get_dis(Rs[i], Cs[i]))
    
    return len(dis_errs)/len(Rs), sum(dis_errs)/len(dis_errs)

def Model_TUB_bb_cs(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim):
    Cs = []
    for i in range(len(Rs)):
        if Ts_cen[i]:
            Cs.append(Ts_cen[i])
        elif Us_cen[i]:
            Cs.append(Us_cen[i])
        elif df.iloc[i]['bb_area'] >= lim:    # 如果 bounding box 面积太大，不予计算
            Cs.append((0, 0))
            continue
        else:
            Cs.append(Bs[i])
    
    dis_errs = []
    for i in range(len(Rs)):
        if Cs[i] != (0, 0):
            dis_errs.append(get_dis(Rs[i], Cs[i]))
    
    return len(dis_errs)/len(Rs), sum(dis_errs)/len(dis_errs)

def Model_TPB_bb_cs(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim):
    Cs = []
    for i in range(len(Rs)):
        if Ts_cen[i]:
            Cs.append(Ts_cen[i])
        elif Ps_cen[i]:
            Cs.append(Ps_cen[i])
        elif df.iloc[i]['bb_area'] >= lim:    # 如果 bounding box 面积太大，不予计算
            Cs.append((0, 0))
            continue
        else:
            Cs.append(Bs[i])
    
    dis_errs = []
    for i in range(len(Rs)):
        if Cs[i] != (0, 0):
            dis_errs.append(get_dis(Rs[i], Cs[i]))
    
    return len(dis_errs)/len(Rs), sum(dis_errs)/len(dis_errs)

def Model_UTB_bb_cs(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim):
    Cs = []
    for i in range(len(Rs)):
        if Us_cen[i]:
            Cs.append(Us_cen[i])
        elif Ts_cen[i]:
            Cs.append(Ts_cen[i])
        elif df.iloc[i]['bb_area'] >= lim:    # 如果 bounding box 面积太大，不予计算
            Cs.append((0, 0))
            continue
        else:
            Cs.append(Bs[i])
    
    dis_errs = []
    for i in range(len(Rs)):
        if Cs[i] != (0, 0):
            dis_errs.append(get_dis(Rs[i], Cs[i]))
    
    return len(dis_errs)/len(Rs), sum(dis_errs)/len(dis_errs)

def Model_UPB_bb_cs(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim):
    Cs = []
    for i in range(len(Rs)):
        if Us_cen[i]:
            Cs.append(Us_cen[i])
        elif Ps_cen[i]:
            Cs.append(Ps_cen[i])
        elif df.iloc[i]['bb_area'] >= lim:    # 如果 bounding box 面积太大，不予计算
            Cs.append((0, 0))
            continue
        else:
            Cs.append(Bs[i])
    
    dis_errs = []
    for i in range(len(Rs)):
        if Cs[i] != (0, 0):
            dis_errs.append(get_dis(Rs[i], Cs[i]))
    
    return len(dis_errs)/len(Rs), sum(dis_errs)/len(dis_errs)

def Model_PTB_bb_cs(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim):
    Cs = []
    for i in range(len(Rs)):
        if Ps_cen[i]:
            Cs.append(Ps_cen[i])
        elif Ts_cen[i]:
            Cs.append(Ts_cen[i])
        elif df.iloc[i]['bb_area'] >= lim:    # 如果 bounding box 面积太大，不予计算
            Cs.append((0, 0))
            continue
        else:
            Cs.append(Bs[i])
    
    dis_errs = []
    for i in range(len(Rs)):
        if Cs[i] != (0, 0):
            dis_errs.append(get_dis(Rs[i], Cs[i]))
    
    return len(dis_errs)/len(Rs), sum(dis_errs)/len(dis_errs)

def Model_PUB_bb_cs(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim):
    Cs = []
    for i in range(len(Rs)):
        if Ps_cen[i]:
            Cs.append(Ps_cen[i])
        elif Us_cen[i]:
            Cs.append(Us_cen[i])
        elif df.iloc[i]['bb_area'] >= lim:    # 如果 bounding box 面积太大，不予计算
            Cs.append((0, 0))
            continue
        else:
            Cs.append(Bs[i])
    
    dis_errs = []
    for i in range(len(Rs)):
        if Cs[i] != (0, 0):
            dis_errs.append(get_dis(Rs[i], Cs[i]))
    
    return len(dis_errs)/len(Rs), sum(dis_errs)/len(dis_errs)

def Model_TB_bb_cs(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim):
    Cs = []
    for i in range(len(Rs)):
        if Ts_cen[i]:
            Cs.append(Ts_cen[i])
        elif df.iloc[i]['bb_area'] >= lim:    # 如果 bounding box 面积太大，不予计算
            Cs.append((0, 0))
            continue
        else:
            Cs.append(Bs[i])
    
    dis_errs = []
    for i in range(len(Rs)):
        if Cs[i] != (0, 0):
            dis_errs.append(get_dis(Rs[i], Cs[i]))
    
    return len(dis_errs)/len(Rs), sum(dis_errs)/len(dis_errs)

def Model_UB_bb_cs(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim):
    Cs = []
    for i in range(len(Rs)):
        if Us_cen[i]:
            Cs.append(Us_cen[i])
        elif df.iloc[i]['bb_area'] >= lim:    # 如果 bounding box 面积太大，不予计算
            Cs.append((0, 0))
            continue
        else:
            Cs.append(Bs[i])
    
    dis_errs = []
    for i in range(len(Rs)):
        if Cs[i] != (0, 0):
            dis_errs.append(get_dis(Rs[i], Cs[i]))
    
    return len(dis_errs)/len(Rs), sum(dis_errs)/len(dis_errs)

def Model_PB_bb_cs(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim):
    Cs = []
    for i in range(len(Rs)):
        if Ps_cen[i]:
            Cs.append(Ps_cen[i])
        elif df.iloc[i]['bb_area'] >= lim:    # 如果 bounding box 面积太大，不予计算
            Cs.append((0, 0))
            continue
        else:
            Cs.append(Bs[i])
    
    dis_errs = []
    for i in range(len(Rs)):
        if Cs[i] != (0, 0):
            dis_errs.append(get_dis(Rs[i], Cs[i]))
    
    return len(dis_errs)/len(Rs), sum(dis_errs)/len(dis_errs)

def Model_B_bb_cs(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim):
    Cs = []
    for i in range(len(Rs)):
        if df.iloc[i]['bb_area'] >= lim:    # 如果 bounding box 面积太大，不予计算
            Cs.append((0, 0))
            continue
        else:
            Cs.append(Bs[i])
    
    dis_errs = []
    for i in range(len(Rs)):
        if Cs[i] != (0, 0):
            dis_errs.append(get_dis(Rs[i], Cs[i]))
    
    return len(dis_errs)/len(Rs), sum(dis_errs)/len(dis_errs)

def Models_bb_dis_errs(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim):
    print("TUPB,", Model_TUPB_bb_cs(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim)[1], ",", \
                   Model_TUPB_bb_cs(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim)[0])
    print("TPUB,", Model_TPUB_bb_cs(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim)[1], ",", \
                   Model_TPUB_bb_cs(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim)[0])
    print("UTPB,", Model_UTPB_bb_cs(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim)[1], ",", \
                   Model_UTPB_bb_cs(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim)[0])
    print("UPTB,", Model_UPTB_bb_cs(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim)[1], ",", \
                   Model_UPTB_bb_cs(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim)[0])
    print("PUTB,", Model_PUTB_bb_cs(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim)[1], ",", \
                   Model_PUTB_bb_cs(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim)[0])
    print("PTUB,", Model_PTUB_bb_cs(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim)[1], ",", \
                   Model_PTUB_bb_cs(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim)[0])
    print()
    print(" TUB,", Model_TUB_bb_cs(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim)[1], ",", \
                   Model_TUB_bb_cs(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim)[0])
    print(" TPB,", Model_TPB_bb_cs(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim)[1], ",", \
                   Model_TPB_bb_cs(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim)[0])
    print(" UTB,", Model_UTB_bb_cs(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim)[1], ",", \
                   Model_UTB_bb_cs(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim)[0])
    print(" UPB,", Model_UPB_bb_cs(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim)[1], ",", \
                   Model_UPB_bb_cs(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim)[0])
    print(" PTB,", Model_PTB_bb_cs(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim)[1], ",", \
                   Model_PTB_bb_cs(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim)[0])
    print(" PUB,", Model_PUB_bb_cs(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim)[1], ",", \
                   Model_PUB_bb_cs(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim)[0])
    print()
    print("  TB,", Model_TB_bb_cs(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim)[1], ",", \
                   Model_TB_bb_cs(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim)[0])
    print("  UB,", Model_UB_bb_cs(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim)[1], ",", \
                   Model_UB_bb_cs(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim)[0])
    print("  PB,", Model_PB_bb_cs(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim)[1], ",", \
                   Model_PB_bb_cs(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim)[0])
    print()
    print("   B,", Model_B_bb_cs(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim)[1], ",", \
                   Model_B_bb_cs(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim)[0])

# median
from statistics import median
def Model_TUPB_median(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim):
    Cs = []
    for i in range(len(Rs)):
        if Ts_cen[i]:
            Cs.append(Ts_cen[i])
        elif Us_cen[i]:
            Cs.append(Us_cen[i])
        elif Ps_cen[i]:
            Cs.append(Ps_cen[i])
        elif df.iloc[i]['bb_area'] >= lim:    # 如果 bounding box 面积太大，不予计算
            Cs.append((0, 0))
            continue
        else:
            Cs.append(Bs[i])
    
    dis_errs = []
    for i in range(len(Rs)):
        if Cs[i] != (0, 0):
            dis_errs.append(get_dis(Rs[i], Cs[i]))
    
    print(median(dis_errs))
def Model_TPUB_median(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim):
    Cs = []
    for i in range(len(Rs)):
        if Ts_cen[i]:
            Cs.append(Ts_cen[i])
        elif Ps_cen[i]:
            Cs.append(Ps_cen[i])
        elif Us_cen[i]:
            Cs.append(Us_cen[i])
        elif df.iloc[i]['bb_area'] >= lim:    # 如果 bounding box 面积太大，不予计算
            Cs.append((0, 0))
            continue
        else:
            Cs.append(Bs[i])
    
    dis_errs = []
    for i in range(len(Rs)):
        if Cs[i] != (0, 0):
            dis_errs.append(get_dis(Rs[i], Cs[i]))
    
    print(median(dis_errs))
def Model_UTPB_median(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim):
    Cs = []
    for i in range(len(Rs)):
        if Us_cen[i]:
            Cs.append(Us_cen[i])
        elif Ts_cen[i]:
            Cs.append(Ts_cen[i])
        elif Ps_cen[i]:
            Cs.append(Ps_cen[i])
        elif df.iloc[i]['bb_area'] >= lim:    # 如果 bounding box 面积太大，不予计算
            Cs.append((0, 0))
            continue
        else:
            Cs.append(Bs[i])
    
    dis_errs = []
    for i in range(len(Rs)):
        if Cs[i] != (0, 0):
            dis_errs.append(get_dis(Rs[i], Cs[i]))
    
    print(median(dis_errs))
def Model_UPTB_median(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim):
    Cs = []
    for i in range(len(Rs)):
        if Us_cen[i]:
            Cs.append(Us_cen[i])
        elif Ps_cen[i]:
            Cs.append(Ps_cen[i])
        elif Ts_cen[i]:
            Cs.append(Ts_cen[i])
        elif df.iloc[i]['bb_area'] >= lim:    # 如果 bounding box 面积太大，不予计算
            Cs.append((0, 0))
            continue
        else:
            Cs.append(Bs[i])
    
    dis_errs = []
    for i in range(len(Rs)):
        if Cs[i] != (0, 0):
            dis_errs.append(get_dis(Rs[i], Cs[i]))
    
    print(median(dis_errs))
def Model_PUTB_median(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim):
    Cs = []
    for i in range(len(Rs)):
        if Ps_cen[i]:
            Cs.append(Ps_cen[i])
        elif Us_cen[i]:
            Cs.append(Us_cen[i])
        elif Ts_cen[i]:
            Cs.append(Ts_cen[i])
        elif df.iloc[i]['bb_area'] >= lim:    # 如果 bounding box 面积太大，不予计算
            Cs.append((0, 0))
            continue
        else:
            Cs.append(Bs[i])
    
    dis_errs = []
    for i in range(len(Rs)):
        if Cs[i] != (0, 0):
            dis_errs.append(get_dis(Rs[i], Cs[i]))
    
    print(median(dis_errs))
def Model_PTUB_median(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim):
    Cs = []
    for i in range(len(Rs)):
        if Ps_cen[i]:
            Cs.append(Ps_cen[i])
        elif Ts_cen[i]:
            Cs.append(Ts_cen[i])
        elif Us_cen[i]:
            Cs.append(Us_cen[i])
        elif df.iloc[i]['bb_area'] >= lim:    # 如果 bounding box 面积太大，不予计算
            Cs.append((0, 0))
            continue
        else:
            Cs.append(Bs[i])
    
    dis_errs = []
    for i in range(len(Rs)):
        if Cs[i] != (0, 0):
            dis_errs.append(get_dis(Rs[i], Cs[i]))
    
    print(median(dis_errs))
def Model_TUB_median(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim):
    Cs = []
    for i in range(len(Rs)):
        if Ts_cen[i]:
            Cs.append(Ts_cen[i])
        elif Us_cen[i]:
            Cs.append(Us_cen[i])
        elif df.iloc[i]['bb_area'] >= lim:    # 如果 bounding box 面积太大，不予计算
            Cs.append((0, 0))
            continue
        else:
            Cs.append(Bs[i])
    
    dis_errs = []
    for i in range(len(Rs)):
        if Cs[i] != (0, 0):
            dis_errs.append(get_dis(Rs[i], Cs[i]))
    
    print(median(dis_errs))
def Model_TPB_median(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim):
    Cs = []
    for i in range(len(Rs)):
        if Ts_cen[i]:
            Cs.append(Ts_cen[i])
        elif Ps_cen[i]:
            Cs.append(Ps_cen[i])
        elif df.iloc[i]['bb_area'] >= lim:    # 如果 bounding box 面积太大，不予计算
            Cs.append((0, 0))
            continue
        else:
            Cs.append(Bs[i])
    
    dis_errs = []
    for i in range(len(Rs)):
        if Cs[i] != (0, 0):
            dis_errs.append(get_dis(Rs[i], Cs[i]))
    
    print(median(dis_errs))
def Model_UTB_median(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim):
    Cs = []
    for i in range(len(Rs)):
        if Us_cen[i]:
            Cs.append(Us_cen[i])
        elif Ts_cen[i]:
            Cs.append(Ts_cen[i])
        elif df.iloc[i]['bb_area'] >= lim:    # 如果 bounding box 面积太大，不予计算
            Cs.append((0, 0))
            continue
        else:
            Cs.append(Bs[i])
    
    dis_errs = []
    for i in range(len(Rs)):
        if Cs[i] != (0, 0):
            dis_errs.append(get_dis(Rs[i], Cs[i]))
    
    print(median(dis_errs))
def Model_UPB_median(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim):
    Cs = []
    for i in range(len(Rs)):
        if Us_cen[i]:
            Cs.append(Us_cen[i])
        elif Ps_cen[i]:
            Cs.append(Ps_cen[i])
        elif df.iloc[i]['bb_area'] >= lim:    # 如果 bounding box 面积太大，不予计算
            Cs.append((0, 0))
            continue
        else:
            Cs.append(Bs[i])
    
    dis_errs = []
    for i in range(len(Rs)):
        if Cs[i] != (0, 0):
            dis_errs.append(get_dis(Rs[i], Cs[i]))
    
    print(median(dis_errs))
def Model_PTB_median(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim):
    Cs = []
    for i in range(len(Rs)):
        if Ps_cen[i]:
            Cs.append(Ps_cen[i])
        elif Ts_cen[i]:
            Cs.append(Ts_cen[i])
        elif df.iloc[i]['bb_area'] >= lim:    # 如果 bounding box 面积太大，不予计算
            Cs.append((0, 0))
            continue
        else:
            Cs.append(Bs[i])
    
    dis_errs = []
    for i in range(len(Rs)):
        if Cs[i] != (0, 0):
            dis_errs.append(get_dis(Rs[i], Cs[i]))
    
    print(median(dis_errs))
def Model_PUB_median(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim):
    Cs = []
    for i in range(len(Rs)):
        if Ps_cen[i]:
            Cs.append(Ps_cen[i])
        elif Us_cen[i]:
            Cs.append(Us_cen[i])
        elif df.iloc[i]['bb_area'] >= lim:    # 如果 bounding box 面积太大，不予计算
            Cs.append((0, 0))
            continue
        else:
            Cs.append(Bs[i])
    
    dis_errs = []
    for i in range(len(Rs)):
        if Cs[i] != (0, 0):
            dis_errs.append(get_dis(Rs[i], Cs[i]))
    
    print(median(dis_errs))
def Model_TB_median(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim):
    Cs = []
    for i in range(len(Rs)):
        if Ts_cen[i]:
            Cs.append(Ts_cen[i])
        elif df.iloc[i]['bb_area'] >= lim:    # 如果 bounding box 面积太大，不予计算
            Cs.append((0, 0))
            continue
        else:
            Cs.append(Bs[i])
    
    dis_errs = []
    for i in range(len(Rs)):
        if Cs[i] != (0, 0):
            dis_errs.append(get_dis(Rs[i], Cs[i]))
    
    print(median(dis_errs))
def Model_UB_median(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim):
    Cs = []
    for i in range(len(Rs)):
        if Us_cen[i]:
            Cs.append(Us_cen[i])
        elif df.iloc[i]['bb_area'] >= lim:    # 如果 bounding box 面积太大，不予计算
            Cs.append((0, 0))
            continue
        else:
            Cs.append(Bs[i])
    
    dis_errs = []
    for i in range(len(Rs)):
        if Cs[i] != (0, 0):
            dis_errs.append(get_dis(Rs[i], Cs[i]))
    
    print(median(dis_errs))
def Model_PB_median(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim):
    Cs = []
    for i in range(len(Rs)):
        if Ps_cen[i]:
            Cs.append(Ps_cen[i])
        elif df.iloc[i]['bb_area'] >= lim:    # 如果 bounding box 面积太大，不予计算
            Cs.append((0, 0))
            continue
        else:
            Cs.append(Bs[i])
    
    dis_errs = []
    for i in range(len(Rs)):
        if Cs[i] != (0, 0):
            dis_errs.append(get_dis(Rs[i], Cs[i]))
    
    print(median(dis_errs))
def Model_B_median(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim):
    Cs = []
    for i in range(len(Rs)):
        if df.iloc[i]['bb_area'] >= lim:    # 如果 bounding box 面积太大，不予计算
            Cs.append((0, 0))
            continue
        else:
            Cs.append(Bs[i])
    
    dis_errs = []
    for i in range(len(Rs)):
        if Cs[i] != (0, 0):
            dis_errs.append(get_dis(Rs[i], Cs[i]))
    
    print(median(dis_errs))
def Models_median(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim):
    Model_TUPB_median(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim)
    Model_TPUB_median(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim)
    Model_UTPB_median(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim)
    Model_UPTB_median(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim)
    Model_PUTB_median(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim)
    Model_PTUB_median(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim)
    Model_TUB_median(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim)
    Model_TPB_median(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim)
    Model_UTB_median(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim)
    Model_UPB_median(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim)
    Model_PTB_median(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim)
    Model_PUB_median(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim)
    Model_TB_median(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim)
    Model_UB_median(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim)
    Model_PB_median(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim)
    Model_B_median(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df, lim)

Rs, Ts_cen, Us_cen, Ps_cen, Bs = processing_area(df_com, df)
Models_bb_dis_errs(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df_com, 5400)
Models_bb_dis_errs(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df_com, 4500)
Models_median(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df_com, 5400)
Models_median(Rs, Ts_cen, Us_cen, Ps_cen, Bs, df_com, 4500)
