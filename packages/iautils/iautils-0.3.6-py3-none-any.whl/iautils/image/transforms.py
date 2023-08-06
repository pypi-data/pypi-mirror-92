########################################################################################################################################
# Image!!!
# iautils.image.transforms
########################################################################################################################################
import numpy as np
import cv2


########################################################################################################################################
## COMPOSE
########################################################################################################################################
class Compose(object):
    """
    Args:
      transforms (list of ``Transform`` objects): list of transforms to compose.

    Example:
      >>> transforms.Compose([
      >>>     transforms.CenterCrop(10),
      >>>     transforms.ToTensor(),
      >>> ])
    """

    def __init__(self, transforms):
        self.transforms = transforms

    def __call__(self, y):
        for t in self.transforms:
            y = t(y)
        return y

    def __repr__(self):
        format_string = self.__class__.__name__ + '('
        for t in self.transforms:
            format_string += '\n'
            format_string += '    {0}'.format(t)
        format_string += '\n)'
        return format_string
    
    
########################################################################################################################################
## IMAGE TRANSFORMATION (Crop, Flip, Rolling, ...)
########################################################################################################################################

################################################################
## ToImage
################################################################
class ToImage(object):
    '''
    shape (H, W) numpy to shape (H, W, 3) w/ dtype uint8 numpy
    (NOTE) 전체 데이터로부터 추정된 x_min, x_max를 사용한 Normalize가 가장 권장 됨
    
    Methods:
      0   Normalize
      1   Standardize along y-axis
    
    Args:
      method         
      x_min, x_max   (for Normalize) use each image's min, max if None
      x_mean, x_std  (for Standardize) use each image's mean, std if None
      z_min, z_max   (for Stardardize) default -2, +2 ~ clip standardize result
      cmap           color map (gray to color) ['magma', 'bone', 'jet', 'winter', ...] ~ see cv2's COLORMAP_*
    
    Returns:
      <np.ndarray> HWC, RGB
    '''
    
    def __init__(self, method=0, x_min=None, x_max=None, x_mean=None, x_std=None, z_min=-2, z_max=2, cmap=None):
        
        self.method = method
        self.x_min, self.x_max = x_min, x_max
        self.x_mean, self.x_std = x_mean, x_std
        self.z_min, self.z_max = z_min, z_max
        self.cmap = eval(f"cv2.COLORMAP_{cmap.upper()}") if cmap is not None else None
        
        # avoid cv2 freeze issue
        cv2.setNumThreads(0)
        
    def __call__(self, x):
        # Normalize
        x = self.convert(x)
        
        # (H x W) to (H x W x C) w/ uint8
        if x.ndim == 2:
            x = np.expand_dims(x, -1)
        x = np.uint8(x * 255)
        
        # Apply Colormap
        if self.cmap is not None:
            x = cv2.applyColorMap(x, self.cmap)
        x = cv2.cvtColor(x, cv2.COLOR_BGR2RGB)            
        
        return x
            
    def convert(self, x):
        # do normalize
        if self.method in [0]:
            x_min = np.min(x) if self.x_min is None else self.x_min
            x_max = np.max(x) if self.x_max is None else self.x_max
            x = (x-x_min)/(x_max-x_min)
            
        # do standardize
        elif self.method in [1]:
            x_mean = np.mean(x) if self.x_mean is None else self.x_mean
            x_std = np.std(x) if self.x_std is None else self.x_std
            x = (x-x_mean)/x_std
            x = (x-self.z_min)/(self.z_max-self.z_min)            
            
        return x
    
    
################################################################
## Square Crop
################################################################
class SquareCrop(object):   
    '''
    모든 변환은 Channel Last 기준 (h x w x c), pytorch에서 사용하려면 (c x h )
    
    init. Args:
      position   ['left', 'center', 'right', 'random']
    '''
    def __init__(self, position='random'):
                
        self.position = position
    
    def __call__(self, x):
        
        if x.ndim == 2:
            x = np.expand_dims(x, -1)
        h, w, c = x.shape
            
        #### if width is smaller than height, drop the data 
        if w <= h:
            return x

        #### do crop
        if self.position == 'left':
            x = x[:, :h, :]
        elif self.position == 'center': 
            x = x[:, w//2-h//2:w//2+h//2, :]
        elif self.position == 'right':
            x = x[:, -h:, :]
        elif self.position == 'random':
            l = np.random.randint(0, w - h)
            x = x[:, l:l+h, :]
        else:
            print('ERROR!!! crop options: [left, center, right, random]')  
                
        return x

    
################################################################
## Resize
################################################################
class Resize(object):
    '''
    모든 변환은 Channel Last 기준 (HWC)
    '''
    def __init__(self, shape=(224, 224), fixed_aspect=True):
        '''
        Args:
          shape         shape after resize
          fixed_aspect
        
        Return:
          <np.ndarray>
        '''

        # 사용자 편의를 위해 - tuple이 아닌 single value가 들어오면 해당 값은 height로 간주
        if not isinstance(shape, tuple):
            shape = (shape, None)
            
        self.height, self.width = shape
        self.fixed_aspect = fixed_aspect
        
        cv2.setNumThreads(0)
        
    def __call__(self, x):
        
        if x.ndim == 2:
            x = np.expand_dims(x, -1)
        h, w, c = x.shape
        
        # set resize width x height
        width, height = self.width, self.height
        if width is None:
            width = int(height * w/h) if self.fixed_aspect else w
        if height is None:
            height = int(width * h/w) if self.fixed_aspect else h
            
        # do resize
        x = cv2.resize(x, (width, height))
        
        return x
    
    
################################################################
## Rolling
################################################################
class Roll(object):
    '''
    모든 변환은 Channel Last 기준 (HWC)
    
    Args:
      shift      'random' or <int>, integer 입력되면 그 값의 pixel만큼 Roll
      direction  roll의 방향 ['x', 'y'] ~ Spectrogram augment에 주로 사용해서 default는 x
      
    Example:
      >>> roll = Roll()
      >>> img_shifted = roll(img)
      
    Returns: 
      <np.ndarray>
    '''
    def __init__(self, freq=0.5, shift='random', direction='x'):

        self.shift = shift
        self.direction = direction.lower()
        self.freq = freq
        
        if self.direction not in ['x', 'y']:
            raise ValueError(f"Input direction not in ['x', 'y']!")
    
    def __call__(self, x):
        if x.ndim == 2:
            x = np.expand_dims(x, -1)
            
        # roll
        if np.random.random() < self.freq:    
            axis = 1 if self.direction in ['x'] else 0   # H: 0, W: 1, C: 2
            max_shift = x.shape[axis]
            
            # do roll
            if isinstance(self.shift, int):
                shift = self.shift
            elif self.shift == 'random':
                shift = np.random.randint(0, max_shift)
            else:
                shift = 0
            
            x = np.roll(x, shift, axis)
            
        return x
        
        
################################################################
## Flip
################################################################
class Flip(object):
    '''
    모든 변환은 Channel Last 기준 (HWC),
    flip의 경우 모든 이미지를 flip하면 학습 결과에 문제가 있으므로 빈도 freq를 지정하도록 함
    
    Args:
      freq       동작 빈도 0 ~ 1
      direction  'x'는 y축 대칭, 'y'는 'x'축 대칭 - default 'x'
      
    Return:
      <np.ndarray>
    '''
    def __init__(self, freq=0.5, direction='x'):
        
        self.freq = freq
        self.direction = direction.lower()
    
    def __call__(self, x):
        
        if x.ndim == 2:
            x = np.expand_dims(x, -1)
        
        # do flip
        if np.random.random() < self.freq:
            x = cv2.flip(x, 1)

        return x
    

################################################################################################################################
# ETC. - API consistency 만족하지 않는 기타 함수
################################################################################################################################

