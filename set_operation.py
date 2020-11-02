import os,glob,sys,shutil

func_name = '&'  #&,|,-,^
file_A = './zhaochi_0913/train/xml/'
file_B = './zhaochi_0913/train/image/'
gen_root_dir = './zhaochi_0913/result/'

def set_operation():
    A_path_list = glob.glob(file_A + '*')
    B_path_list = glob.glob(file_B + '*')
    A_name_list = [(os.path.split(a_path)[-1]).strip()[:-4] for a_path in A_path_list]
    B_name_list = [(os.path.split(a_path)[-1]).strip()[:-4] for a_path in B_path_list]
    A_name_list = set(A_name_list)
    B_name_list = set(B_name_list)
    print('len(A_name_list):',len(A_name_list))
    #print(A_name_list)
    print('len(B_name_list):',len(B_name_list))
    #print(B_name_list)
    #print(len(A_name_list - B_name_list))
    print('set operation:',func_name)
    results_list = []    
    if func_name == '&':
        results_list.extend(A_name_list & B_name_list)
    elif func_name == '|':
        results_list.append(A_name_list)
        results_list.append(B_name_list - A_name_list)
    elif func_name == '-':
        results_list.append(A_name_list - B_name_list)
    elif func_name == '^':
        results_list.append(A_name_list - B_name_list)
        results_list.append(B_name_list - A_name_list)
    #print(results_list)
    return results_list

def move_file():
    results_list = set_operation()
    if results_list :
        if os.path.exists(gen_root_dir):
            shutil.rmtree(gen_root_dir)
        os.makedirs(gen_root_dir)
        if func_name == '&':
            gen_A_file = gen_root_dir + 'A/'
            gen_B_file = gen_root_dir + 'B/'
            os.makedirs(gen_A_file)
            os.makedirs(gen_B_file)
            for a_result in results_list:
                A_files = glob.glob(file_A + a_result + '.*')
                B_files = glob.glob(file_B + a_result + '.*')
                for a_A_file in A_files:
                    shutil.copyfile(a_A_file , gen_A_file + os.path.split(a_A_file)[-1])
                for a_B_file in B_files:
                    shutil.copyfile(a_B_file , gen_B_file + os.path.split(a_B_file)[-1])
        else:
            if len(results_list) == 1:
                #print(len(results_list[0]))
                for a_result in results_list[0]:
                    files = glob.glob(file_A + a_result + '.*')
                    #print(files)
                    for a_file in files:
                       shutil.copyfile(a_file , gen_root_dir + os.path.split(a_file)[-1])
            elif len(results_list) == 2:
                A_results = results_list[0]
                B_results = results_list[1]
                for a_result in A_results:
                    A_files = glob.glob(file_A + a_result + '.*')
                    for a_A_file in A_files:
                        shutil.copyfile(a_A_file , gen_root_dir + os.path.split(a_A_file)[-1])
                for a_result in B_results:
                    B_files = glob.glob(file_B + a_result + '.*')
                    for a_B_file in B_files:
                        shutil.copyfile(a_B_file , gen_root_dir + os.path.split(a_B_file)[-1])

def main():
    print('start')
    move_file()
    print('end')

if __name__ == '__main__':
    main()    
