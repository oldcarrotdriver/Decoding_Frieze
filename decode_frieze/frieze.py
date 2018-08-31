from copy import deepcopy
from math import sqrt
from collections import defaultdict


class FriezeError(Exception):
    def __init__(self, message):
        self.message = message
    

class Frieze:
    def __init__(self, file_name):
        self.file_name = file_name
        
        
        
        self.nb_of_period = 0
        self.grid = self.decode_into_grid()
        self.copy_grid = deepcopy(self.grid)
        self.north_grid = [[0 for _ in range(len(self.grid[0]))] for _ in range(len(self.grid))]
        self.northeast_grid = [[0 for _ in range(len(self.grid[0]))] for _ in range(len(self.grid))]
        self.east_grid = [[0 for _ in range(len(self.grid[0]))] for _ in range(len(self.grid))]
        self.southeast_grid = [[0 for _ in range(len(self.grid[0]))] for _ in range(len(self.grid))]
        self.decomposite_into_four_direction()
        self.draw_north = self.draw_north_line()
        self.draw_northeast = self.draw_northeast_line()
        self.draw_southeast = self.draw_southeast_line()
        self.draw_east = self.draw_east_line()
        self.is_horizontal = self.is_horizontal_reflection()
        self.is_vertical = self.is_vertical_reflection()
        self.is_glided = self.is_glided_reflection()
        self.is_rotation = self.is_rotation_reflection()
        
    
    
    def lcm_of_a_list(self, list_x):
        max_period_number = max(list_x)
        try_nb = deepcopy(max_period_number)
        index = 0
        multiplier = 2
        while index != len(list_x):
            if try_nb % int(list_x[index]) == 0:
                index += 1
            else:
                try_nb = max_period_number * multiplier
                index = 0
                multiplier += 1
        return try_nb
        
        
    def decode_into_grid(self):
        set_of_valid_number = {'0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15'}
        with open(self.file_name) as opened_file:
            grid = opened_file.readlines()
            grid = [items.strip('\n') for items in grid]
            grid = [items.split(' ') for items in grid]
            new_grid = []
            one_line = []
            for nb_of_line in range(len(grid)):
                for items in range(len(grid[nb_of_line])): 
                    if grid[nb_of_line][items] == '':
                        continue
                    one_line.append(grid[nb_of_line][items])
                if one_line != []:
                    new_grid.append(one_line)
                    one_line = []
                    
        lenth_of_height = len(new_grid)
        if lenth_of_height > 17 or lenth_of_height < 3:
            raise FriezeError('Incorrect input.')
        lenth_of_width = len(new_grid[0])
        if lenth_of_width > 51 or lenth_of_width < 5:
            raise FriezeError('Incorrect input.')
        for i in range(lenth_of_height):
            if len(new_grid[i]) != lenth_of_width:
                raise FriezeError('Incorrect input.')
            for j in range(len(new_grid[i])):
                if new_grid[i][j] not in set_of_valid_number:
                    raise FriezeError('Incorrect input.')
        
        set_of_number_includes_2 = {'2','3','6','7','10','11','14','15'}
        
        if new_grid[0][lenth_of_width-1] != '0':
            raise FriezeError('Input does not represent a frieze.')
        for i in range(lenth_of_width - 1):
            if new_grid[0][i] not in {'4', '12'}:
                raise FriezeError('Input does not represent a frieze.')
            if int(new_grid[0][i]) >= 8 and (new_grid[1][i] in set_of_number_includes_2):
                raise FriezeError('Input does not represent a frieze.')
        for i in range(1, lenth_of_height):
            if (new_grid[i][lenth_of_width-1] not in {'0', '1'}) or\
                    ((int(new_grid[i][0]) % 2) != (int(new_grid[i][lenth_of_width-1]) % 2)):
                raise FriezeError('Input does not represent a frieze.')
        for i in range(lenth_of_width - 1):
            if int(new_grid[lenth_of_height-1][i]) >= 8 or int(new_grid[lenth_of_height-1][i]) < 4:
                raise FriezeError('Input does not represent a frieze.')
        
        for i in range(1, lenth_of_height - 1):
            for j in range(lenth_of_width - 1):
                if int(new_grid[i][j]) >= 8 and (new_grid[i+1][j] in set_of_number_includes_2):
                    raise FriezeError('Input does not represent a frieze.')
        
        
        list_of_period = []
        whole_repeated_lenth = lenth_of_width - 1
        calculated_rows_index = set()
        list_of_second_possible_divider = []
        for possible_divider in range(1, round(sqrt(whole_repeated_lenth)) + 1):
            if whole_repeated_lenth % possible_divider == 0:
                list_of_second_possible_divider.append(whole_repeated_lenth // possible_divider)
                for rows in range(lenth_of_height):
                    if rows in calculated_rows_index:
                        continue
                    possible_period = new_grid[rows][0: possible_divider]
                    candidate_period_nb = len(possible_period)
                    for start_point in range(possible_divider, whole_repeated_lenth, possible_divider):
                        if new_grid[rows][start_point: start_point+possible_divider] != possible_period:
                            candidate_period_nb = 0
                            break
                            
                    if candidate_period_nb == 0:
                        continue
                    else:
                        list_of_period.append(candidate_period_nb)
                        calculated_rows_index.add(rows)
                        
        if len(calculated_rows_index) != lenth_of_height:
            for possible_divider in sorted(list_of_second_possible_divider):
                if possible_divider > whole_repeated_lenth // 2:
                    break
                for rows in range(lenth_of_height):
                    if rows in calculated_rows_index:
                        continue
                    possible_period = new_grid[rows][0: possible_divider]
                    candidate_period_nb = len(possible_period)
                    for start_point in range(possible_divider, whole_repeated_lenth, possible_divider):
                        if new_grid[rows][start_point: start_point+possible_divider] != possible_period:
                            candidate_period_nb = 0
                            break
                    if candidate_period_nb == 0:
                        continue
                    else:
                        list_of_period.append(candidate_period_nb)
                        calculated_rows_index.add(rows)
            if len(calculated_rows_index) != lenth_of_height:
                raise FriezeError('Input does not represent a frieze.')
        
        #print(list_of_period)
        the_period = self.lcm_of_a_list(list_of_period)
        
        if the_period > whole_repeated_lenth // 2 or the_period < 2:
            raise FriezeError('Input does not represent a frieze.')
        
        self.nb_of_period = the_period
        return new_grid
    

                
    def decomposite_into_four_direction(self):
        for i in range(len(self.copy_grid)):
            for j in range(len(self.copy_grid[0])):
                #print((i,j))
                if int(self.copy_grid[i][j]) >= 8:
                    self.copy_grid[i][j] = int(self.copy_grid[i][j]) - 8
                    self.southeast_grid[i][j] = 1
                if int(self.copy_grid[i][j]) >= 4:
                    self.copy_grid[i][j] = int(self.copy_grid[i][j]) - 4
                    self.east_grid[i][j] = 1
                if int(self.copy_grid[i][j]) >= 2:
                    self.copy_grid[i][j] = int(self.copy_grid[i][j]) - 2
                    self.northeast_grid[i][j] = 1
                if int(self.copy_grid[i][j]) >= 1:
                    self.copy_grid[i][j] = int(self.copy_grid[i][j]) - 1
                    self.north_grid[i][j] = 1

        
    def draw_north_line(self):
        output_str = []
        for i in range(len(self.grid[0])):
            for j in range(len(self.grid)):
                if self.north_grid[j][i] == 1 and self.north_grid[j-1][i] == 0:
                    start_point = f'({i},{j-1})'
                if j + 1 == len(self.grid):
                    if self.north_grid[j][i] == 1:
                        end_point = f'({i},{j})'
                        output_str.append(f'{start_point} -- {end_point}')
                        start_point = ''
                        end_point = ''
                elif self.north_grid[j][i] == 1 and self.north_grid[j+1][i] == 0:
                        end_point = f'({i},{j})'
                        output_str.append(f'{start_point} -- {end_point}')
                        start_point = ''
                        end_point = ''
        return output_str
    
    def draw_east_line(self):
        output_str = []
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0]) - 1):
                if self.east_grid[i][j] == 0:
                    continue
                if self.east_grid[i][j] == 1 and j == 0:
                    start_point = f'({j},{i})'
                elif self.east_grid[i][j] == 1 and self.east_grid[i][j-1] == 0:
                    start_point = f'({j},{i})'
                if self.east_grid[i][j] == 1 and self.east_grid[i][j+1] == 0:
                    end_point = f'({j+1},{i})'
                    output_str.append(f'{start_point} -- {end_point}')
                    start_point = ''
                    end_point = ''
        return output_str
    
    def draw_northeast_line(self):
        output_str = []
        dic_of_rootpoint = defaultdict(list)
        lenth_of_height = len(self.grid)
        lenth_of_width = len(self.grid[0])
        for i in range(lenth_of_height-1, 0, -1):
            for j in range(lenth_of_width-1):
                if self.northeast_grid[i][j] == 1 and (i == lenth_of_height - 1 or j == 0):
                    dic_of_rootpoint[(j, i)] = [(j+1, i-1)]
                elif self.northeast_grid[i][j] == 1 and self.northeast_grid[i+1][j-1] == 0:
                    dic_of_rootpoint[(j, i)] = [(j+1, i-1)]
                elif self.northeast_grid[i][j] == 1 and self.northeast_grid[i+1][j-1] == 1:
                    if (j-1, i+1) in dic_of_rootpoint:
                        dic_of_rootpoint[(j-1, i+1)].append(((j+1, i-1)))
                    else:
                        for roots in dic_of_rootpoint:
                            if (j, i) in set(dic_of_rootpoint[roots]):
                                dic_of_rootpoint[roots].append((j+1, i-1))
                                break
        queue = sorted(dic_of_rootpoint)
        queue_of_line = sorted(queue, key = lambda x: x[1])
        #print(queue_of_line)
        for start_point in queue_of_line:
            output_str.append(f'({start_point[0]},{start_point[1]}) -- ({dic_of_rootpoint[start_point][-1][0]},{dic_of_rootpoint[start_point][-1][1]})')
        return output_str
    
    
    def draw_southeast_line(self):
        output_str = []
        dic_of_rootpoint = defaultdict(list)
        lenth_of_height = len(self.grid)
        lenth_of_width = len(self.grid[0])
        for i in range(lenth_of_height-1):
            for j in range(lenth_of_width-1):
                if self.southeast_grid[i][j] == 1 and (i == 0 or j == 0):
                    dic_of_rootpoint[(j, i)] = [(j+1, i+1)]
                elif self.southeast_grid[i][j] == 1 and self.southeast_grid[i-1][j-1] == 0:
                    dic_of_rootpoint[(j, i)] = [(j+1, i+1)]
                elif self.southeast_grid[i][j] == 1 and self.southeast_grid[i-1][j-1] == 1:
                    if (j-1, i-1) in dic_of_rootpoint:
                        dic_of_rootpoint[(j-1, i-1)].append(((j+1, i+1)))
                    else:
                        for roots in dic_of_rootpoint:
                            if (j, i) in set(dic_of_rootpoint[roots]):
                                dic_of_rootpoint[roots].append((j+1, i+1))
                                break
        queue = sorted(dic_of_rootpoint)
        queue_of_line = sorted(queue, key = lambda x: x[1])
        for start_point in queue_of_line:
            output_str.append(f'({start_point[0]},{start_point[1]}) -- ({dic_of_rootpoint[start_point][-1][0]},{dic_of_rootpoint[start_point][-1][1]})')
        return output_str
    
    
    def is_horizontal_reflection(self):
        width = self.nb_of_period
        height = len(self.grid)
        if height % 2 == 0:
            for i in range(height // 2):
                for j in range(width):
                    #east
                    if self.east_grid[i][j] != self.east_grid[height-i-1][j]:
                        return False
                    #north
                    if i != 0:
                        if self.north_grid[i][j] != self.north_grid[height-i][j]:
                            return False
                        #northeast
                        if self.northeast_grid[i][j] != self.southeast_grid[height-i-1][j]:
                            return False
                    #southeast
                    if self.southeast_grid[i][j] != self.northeast_grid[height-i-1][j]:
                        return False
            return True
        else:
            for i in range(height // 2 + 1):
                for j in range(width):
                    #east
                    if self.east_grid[i][j] != self.east_grid[height-i-1][j]:
                        return False
                    #north
                    if i != 0:
                        if self.north_grid[i][j] != self.north_grid[height-i][j]:
                            return False
                        #northeast
                        if self.northeast_grid[i][j] != self.southeast_grid[height-i-1][j]:
                            return False
                    #southeast
                    if self.southeast_grid[i][j] != self.northeast_grid[height-i-1][j]:
                        return False
            return True
            
            
    def is_vertical_reflection_single(self, start_point, width):
#         width = self.nb_of_period
        height = len(self.grid)
        if width % 2 == 0:
            for i in range(height):
                for j in range(start_point, start_point + width):
                    #north
                    if self.north_grid[i][j] != self.north_grid[i][2*start_point+width-j-1]:
                        return False
                    #east
                    if start_point != 0 or (start_point == 0 and j != start_point + width - 1):
                        if self.east_grid[i][j] != self.east_grid[i][2*start_point+width-2-j]:
                            return False
                        #northeast
                        if i != 0:
                            if self.northeast_grid[i][j] != self.southeast_grid[i-1][2*start_point+width-2-j]:
                                return False
                        #southeast
                        if i != height - 1:
                            if self.southeast_grid[i][j] != self.northeast_grid[i+1][2*start_point+width-2-j]:
                                return False
                    if start_point == 0 and j == start_point + width - 1:
                        if self.east_grid[i][j] != self.east_grid[i][-2]:
                            return False
                        #northeast
                        if i != 0:
                            if self.northeast_grid[i][j] != self.southeast_grid[i-1][-2]:
                                return False
                        #southeast
                        if i != height - 1:
                            if self.southeast_grid[i][j] != self.northeast_grid[i+1][-2]:
                                return False
                        
            return True
        else:
            for i in range(height):
                for j in range(start_point, start_point + width):
                    #north
                    if self.north_grid[i][j] != self.north_grid[i][2*start_point+width-j-1]:
                        return False
                    #east
                    if start_point != 0 or (start_point == 0 and j != start_point + width - 1):
                        if self.east_grid[i][j] != self.east_grid[i][2*start_point+width-2-j]:
                            return False
                        #northeast
                        if i != 0:
                            if self.northeast_grid[i][j] != self.southeast_grid[i-1][2*start_point+width-2-j]:
                                return False
                        #southeast
                        if i != height - 1:
                            if self.southeast_grid[i][j] != self.northeast_grid[i+1][2*start_point+width-2-j]:
                                return False
                    if start_point == 0 and j == start_point + width - 1:
                        if self.east_grid[i][j] != self.east_grid[i][-2]:
                            return False
                        #northeast
                        if i != 0:
                            if self.northeast_grid[i][j] != self.southeast_grid[i-1][-2]:
                                return False
                        #southeast
                        if i != height - 1:
                            if self.southeast_grid[i][j] != self.northeast_grid[i+1][-2]:
                                return False
            return True
        
    def is_vertical_reflection(self):
        width = self.nb_of_period
        for start_point in range(width):
            if self.is_vertical_reflection_single(start_point, width) is True:
                return True
        width = self.nb_of_period + 1
        for start_point in range(width):
            if self.is_vertical_reflection_single(start_point, width) is True:
                return True
        return False
    
    
    def is_glided_reflection(self):
        if self.nb_of_period % 2 != 0:
            return False
        half_period = self.nb_of_period // 2
        width = self.nb_of_period
        height = len(self.grid)
        if height % 2 == 0:
            for i in range(height // 2):
                for j in range(half_period, half_period + width):
                    #east
                    if self.east_grid[i][j] != self.east_grid[height-i-1][j-half_period]:
                        return False
                    #north
                    if i != 0:
                        if self.north_grid[i][j] != self.north_grid[height-i][j-half_period]:
                            return False
                        #northeast
                        if self.northeast_grid[i][j] != self.southeast_grid[height-i-1][j-half_period]:
                            return False
                    #southeast
                    if self.southeast_grid[i][j] != self.northeast_grid[height-i-1][j-half_period]:
                        return False
            return True
        else:
            for i in range(height // 2 + 1):
                for j in range(half_period, half_period + width):
                    #east
                    if self.east_grid[i][j] != self.east_grid[height-i-1][j-half_period]:
                        return False
                    #north
                    if i != 0:
                        if self.north_grid[i][j] != self.north_grid[height-i][j-half_period]:
                            return False
                        #northeast
                        if self.northeast_grid[i][j] != self.southeast_grid[height-i-1][j-half_period]:
                            return False
                    #southeast
                    if self.southeast_grid[i][j] != self.northeast_grid[height-i-1][j-half_period]:
                        return False
            return True
        
    def is_rotation_reflection_single(self, start_point, width):
        height = len(self.grid)
        if height % 2 == 0:
            for i in range(height // 2):
                for j in range(start_point, start_point + width + 1):
                    #north
                    if i != 0:
                        if self.north_grid[i][j] != self.north_grid[height-i][2*start_point+width-j]:
                            return False
                        #northeast
                        if j != start_point + width:
                            if self.northeast_grid[i][j] != self.northeast_grid[height-i][2*start_point+width-j-1]:
                                return False
                    #east
                    if j != start_point + width:
                        if self.east_grid[i][j] != self.east_grid[height-1-i][2*start_point+width-j-1]:
                            return False
                        #southeast
                        if self.southeast_grid[i][j] != self.southeast_grid[height-2-i][2*start_point+width-j-1]:
                            return False
            return True
        else:
            for i in range(height // 2 + 1):
                for j in range(start_point, start_point + width + 1):
                    #north
                    if i != 0:
                        if self.north_grid[i][j] != self.north_grid[height-i][2*start_point+width-j]:
                            return False
                        #northeast
                        if j != start_point + width:
                            if self.northeast_grid[i][j] != self.northeast_grid[height-i][2*start_point+width-j-1]:
                                return False
                    #east
                    if j != start_point + width:
                        if self.east_grid[i][j] != self.east_grid[height-1-i][2*start_point+width-j-1]:
                            return False
                        #southeast
                        if self.southeast_grid[i][j] != self.southeast_grid[height-2-i][2*start_point+width-j-1]:
                            return False
            return True
    
    def is_rotation_reflection(self):
        width = self.nb_of_period
        for start_point in range(width):
            if self.is_rotation_reflection_single(start_point, width) is True:
                return True
        width = self.nb_of_period + 1
        for start_point in range(width):
            if self.is_rotation_reflection_single(start_point, width) is True:
                return True
        return False
    
    def analyse(self):
        if self.is_horizontal and not self.is_vertical and not self.is_glided and not self.is_rotation:
            print(f'Pattern is a frieze of period {self.nb_of_period} that is invariant under translation')
            print('        and horizontal reflection only.')
        if self.is_vertical and not self.is_horizontal and not self.is_glided and not self.is_rotation:
            print(f'Pattern is a frieze of period {self.nb_of_period} that is invariant under translation')
            print('        and vertical reflection only.')
        if self.is_glided and not self.is_vertical and not self.is_horizontal and not self.is_rotation:
            print(f'Pattern is a frieze of period {self.nb_of_period} that is invariant under translation')
            print('        and glided horizontal reflection only.')
        if self.is_rotation and not self.is_vertical and not self.is_horizontal and not self.is_glided:
            print(f'Pattern is a frieze of period {self.nb_of_period} that is invariant under translation')
            print('        and rotation only.')
        if (self.is_vertical and self.is_glided) or (self.is_rotation and self.is_glided):
            print(f'Pattern is a frieze of period {self.nb_of_period} that is invariant under translation,')
            print('        glided horizontal and vertical reflections, and rotation only.')
        if (self.is_vertical and self.is_horizontal) or (self.is_rotation and self.is_horizontal):
            print(f'Pattern is a frieze of period {self.nb_of_period} that is invariant under translation,')
            print('        horizontal and vertical reflections, and rotation only.')
        if not self.is_horizontal and not self.is_vertical and not self.is_glided and not self.is_rotation:
            print(f'Pattern is a frieze of period {self.nb_of_period} that is invariant under translation only.')
            
            
    def display(self):
        top_components = [
            r'\documentclass[10pt]{article}',
            r'\usepackage{tikz}',
            r'\usepackage[margin=0cm]{geometry}',
            r'\pagestyle{empty}',
            r'',
            r'\begin{document}',
            '',
            r'\vspace*{\fill}',
            r'\begin{center}',
            r'\begin{tikzpicture}[x=0.2cm, y=-0.2cm, thick, purple]',
            '% North to South lines'
        ]
        end_components = [
            r'\end{tikzpicture}',
            r'\end{center}',
            r'\vspace*{\fill}',
            '',
            r'\end{document}'
        ]
        with open(f'{self.file_name[: -4]}.tex', 'w') as opened_file:
            for rows in top_components:
                opened_file.write(f'{rows}\n')
            if self.draw_north != []:
                for rows in self.draw_north:
                    opened_file.write(f'    \draw {rows};\n')
            opened_file.write('% North-West to South-East lines\n')
            if self.draw_southeast != []:
                for rows in self.draw_southeast:
                    opened_file.write(f'    \draw {rows};\n')
            opened_file.write('% West to East lines\n')
            if self.draw_east != []:
                for rows in self.draw_east:
                    opened_file.write(f'    \draw {rows};\n')
            opened_file.write('% South-West to North-East lines\n')
            if self.draw_northeast != []:
                for rows in self.draw_northeast:
                    opened_file.write(f'    \draw {rows};\n')
            for rows in end_components:
                opened_file.write(f'{rows}\n')


