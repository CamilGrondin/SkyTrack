print("TC = Surface position")
                
                if HEX_ARRAY and HEX_ARRAY[0] == HEX:
                    print("Already received")
                    HEX_ARRAY.pop(0)
                HEX_ARRAY.append(HEX)
                    
                # print(HEX_ARRAY)
                MOV = ME[5:12]
                print("Movement : ", end="")
                print(ME[5:12])
                if(int(MOV, 2) == 0):
                    print("Speed not available")
                elif(int(MOV, 2) == 1):
                    print("Stopped (v < 0.125 kt)")
                elif(2 <= int(MOV, 2) <= 8):
                    print("0.125 ≤ v < 1 kt")
                elif(9 <= int(MOV, 2) <= 12):
                    print("1 kt ≤ v < 2 kt")
                elif(13 <= int(MOV, 2) <= 38):
                    print("2 kt ≤ v < 15 kt")
                elif(39 <= int(MOV, 2) <= 93):
                    print("15 kt ≤ v < 70 kt")
                elif(94 <= int(MOV, 2) <= 108):
                    print("70 kt ≤ v < 100 kt")
                elif(109 <= int(MOV, 2) <= 123):
                    print("100 kt ≤ v < 175 kt")
                elif(int(MOV, 2) == 124):
                    print("v ≥ 175 kt")
                elif(125 <= int(MOV, 2) <= 127):
                    print("Reserved")

                S = ME[12:13]
                if(int(S, 2) == 0):
                    print("The ground track fields is invalid")
                elif(int(S, 2) == 1):
                    n = int(ME[13:20], 2)
                    X = 360 * n / 128
                    print("Ground track : " + str(X) + "°")
                
                MSG_HEX = HEX_ARRAY[0]
                MSG = bin(int(MSG_HEX, 16))[2:]
                
                ME2 = BITS2[32:88]

                print("Time : ", end="")
                T = ME[20:21]
                T2 = ME2[20:21]
                print(int(ME[20:21], 2), end=", ")
                print(int(ME2[20:21], 2))

                print("CPR Format : ", end="")
                F = MSG[53:54]
                if(int(F, 2) == 0):
                    print("even frame")
                elif(int(F, 2) == 1):
                    print("odd frame")
                    print("---")
                    print("Les valeurs de latitude et longitude sont inversées")
                    HEX_ARRAY.pop(0)
                    print("---")

                print("Encoded latitude : ", end="")
                lat_cpr_enc_even = int(ME[22:39], 2)
                print(lat_cpr_enc_even, end=", ")
                lat_cpr_enc_odd = int(ME2[22:39], 2)
                print(lat_cpr_enc_odd)

                print("Encoded longitude : ", end="")
                lon_cpr_enc_even = int(ME[39:56], 2)
                print(lon_cpr_enc_even, end=", ")
                lon_cpr_enc_odd = int(ME2[39:56], 2)
                print(lon_cpr_enc_odd)

                print(" ")

                lat_cpr_even = lat_cpr_enc_even / 2**17
                lon_cpr_even = lon_cpr_enc_even / 2**17

                lat_cpr_odd = lat_cpr_enc_odd / 2**17
                lon_cpr_odd = lon_cpr_enc_odd / 2**17

                dLat_even = 90 / (4 * Nz)
                dLat_odd = 90 / (4 * Nz - 1)
                
                print(lat_cpr_enc_even)
                print(lat_cpr_enc_odd)
                print(lat_cpr_even)
                print(lat_cpr_odd)
                
                j = floor(59 * lat_cpr_even - 60 * (lat_cpr_odd) + 0.5)
                
                lat_even = dLat_even * ((j % 60) + lat_cpr_even)
                lat_odd = dLat_odd * ((j % 59) + lat_cpr_odd)

                if(lat_even >= 270):
                    lat_even = lat_even - 360
                if(lat_odd >= 270):
                    lat_odd = lat_odd - 360

                if(NL(lat_even) != NL(lat_odd)):
                    print("---")
                    print("The pair of messages are from different longitude zones, and it is not possible to compute the correct global position.")
                    print("---")

                lat = lat_odd # because the 2nd message is the most recent

                lat_S = lat - 90

                if abs(lat - ref_lat) <= abs(lat_S - ref_lat):
                    print("Latitude : ", end="")
                    print(round(lat, 6), end=" N")
                    lat = lat
                else:
                    print("Latitude : ", end="")
                    print(round(lat_S, 6), end=" S")
                    lat = lat_S
                print(" ")

                m = floor(lon_cpr_even * (NL(lat) - 1) - lon_cpr_odd * NL(lat) + 0.5)

                n_even = max(NL(lat), 1)
                n_odd = max(NL(lat) - 1, 1)

                dLon_even = 90 / n_even
                dLon_odd = 90 / n_odd

                lon_even = dLon_even * (m % n_even + lon_cpr_even)
                lon_odd = dLon_odd * (m % n_odd + lon_cpr_odd)
                
                lon1 = lon_odd # because the 2nd message is the most recent

                lon2 = lon1 + 90
                lon3 = lon1 + 180
                lon4 = lon1 + 270

                print("Longitude : ", end="")
                lon_candidates = [lon1, lon2, lon3, lon4]
                lon = min(lon_candidates, key=lambda x: abs(x - ref_lon))
                if lon >= 0:
                    print(round(lon, 6), end=" E")
                print(" ")

                # Locally unambiguous decoding
                # Trier les signaux par rapport à leur parité