# Calculate numbers of tweets based on different area
def model_bb(df_com, lim):
    diss = []
    count = 0
    for i in range(len(df_com)):
        if float(df_com.iloc[i]['bb_area']) <= lim:
            count += 1
            diss.append(distance(float(df_com.iloc[i]['co_lon']), float(df_com.iloc[i]['co_lat']), \
                       float(df_com.iloc[i]['pb_avg_lon']), float(df_com.iloc[i]['pb_avg_lat'])))
    print(sum(diss)/count)
    print(count)
    print()
    
model_bb(df_com, 1760000)
model_bb(df_com, 176000)
model_bb(df_com, 17600)
model_bb(df_com, 8200)
model_bb(df_com, 6800)
model_bb(df_com, 5500)
model_bb(df_com, 5400)
model_bb(df_com, 4500)
model_bb(df_com, 2000)
model_bb(df_com, 900)
model_bb(df_com, 800)
model_bb(df_com, 250)
model_bb(df_com, 20)
model_bb(df_com, 20)
model_bb(df_com, 5)
