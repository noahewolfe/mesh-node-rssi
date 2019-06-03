def plot_contour_from_points(x, y):
    import scipy.stats
    import numpy as np
    import pylab as pl

    xmin = 0.0
    xmax = 10.0
    ymin = 0.0
    ymax = 10.0
    
    #m1 = np.random.uniform(xmin, xmax, size=100)
    #m2 = np.random.uniform(ymin, ymax, size=100)
    
    # density estimation stuff
    X, Y = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]                                                     
    positions = np.vstack([X.ravel(), Y.ravel()])                                                       
    values = np.vstack([m1, m2])                                
    kernel = scipy.stats.gaussian_kde(values)                                                                 
    Z = np.reshape(kernel(positions).T, X.shape)
        
    fig, ax = pl.subplots()                   
    
    # Show density 
    ax.imshow(np.rot90(Z), cmap=pl.cm.gist_earth_r,                                                    
              extent=[xmin, xmax, ymin, ymax])
    
    # Add contour lines
    pl.contour(X, Y, Z)                                                                           
    
    ax.plot(m1, m2, 'k.', markersize=2)    
    
    ax.set_xlim([xmin, xmax])                                                                           
    ax.set_ylim([ymin, ymax])                                                                           
    pl.show()