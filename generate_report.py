import pyemma
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import numpy as np

def make_plots(dtrajs,tica,tica_output,msm,project_name):
    # make initial plots
    plot_trajectory_length_histogram(dtrajs,project_name)

    # make tICA plots
    inspect_tica(tica,project_name)
    plot_tics(tica_output,n_tics=10,project_name=project_name)

    # make MSM plots
    plot_sanity_check(msm)
    compute_its(dtrajs,project_name)
    plot_timescales(msm,project_name)

    # coarse-grain
    n_states = estimate_n_macrostates(msm)
    hmm = msm.coarse_grain(n_states)

    # make HMM plots
    plot_free_energies(hmm)

    # sample from macrostates
    # to-do!
    # follow: http://www.emma-project.org/latest/generated/MSM_BPTI.html#representative-structures

def inspect_tica(tica,project_name):
    # plot cumulative kinetic variance explained
    eigs = tica.eigenvalues
    plt.figure()
    plt.plot(np.cumsum(eigs**2))
    plt.xlabel('# tICA eigenvalues')
    plt.ylabel('Cumulative sum of tICA eigenvalues squared')
    plt.title('Cumulative "kinetic variance" explained')
    plt.savefig('{0}_tica_kinetic_variance.jpg'.format(project_name),dpi=300)
    plt.close()

def plot_tics(Y,n_tics,project_name):
    import corner
    plt.figure()
    Y_ = np.vstack(Y)[:,:n_tics]
    labels = ['tIC{0}'.format(i+1) for i in range(Y_.shape[1])]
    corner.corner(Y_,labels=labels,bins=50)
    #plt.title('{0}:\nProjection onto top-{1} tICs'.format(project_name,len(labels)))
    plt.savefig('{0}_tica_projection.jpg'.format(project_name),dpi=300)
    plt.close()

def plot_sanity_check(msm):
    ''' Plot stationary distribution vs. counts'''
    statdist = msm.stationary_distribution
    relative_counts = msm.count_matrix_active.sum(0)/np.sum(msm.count_matrix_active)

    plt.figure()
    plt.scatter(statdist,relative_counts)
    plt.xlabel('MSM stationary distribution')
    plt.ylabel('Relative counts')
    plt.savefig('{0}_sanity_check.jpg'.format(project_name),dpi=300)
    plt.close()

def plot_trajectory_length_histogram(dtrajs,project_name):
    lens = []
    for dtraj in dtrajs:
        lens.append(len(dtraj))
    plt.figure()
    plt.hist(lens,bins=50);
    plt.xlabel('Trajectory length')
    plt.ylabel('Occurrences')
    plt.title('Distribution of trajectory lengths')
    plt.savefig('{0}_traj_length_histogram.jpg'.format(project_name),dpi=300)
    plt.close()

def plot_timescales(msm,project_name):
    plt.figure()
    plt.plot(m.timescales()/4,'.')
    plt.xlabel('Timescale index')
    plt.ylabel('Timescale (ns)')
    plt.title('{0}: Timescales'.format(project_name))
    plt.savefig('{0}_timescales.jpg'.format(project_name),dpi=300)
    plt.close()

def compute_its(dtrajs,project_name):
    # select lag-time for MSM estimation:
    # we're looking for the earliest lag-time where these curves flatten out

    lag_sets = [range(1,101),range(1,1001)[::10]]
    for i,lags in enumerate(lag_sets):
        its = pyemma.msm.its(dtrajs,lags,nits=20,errors='bayes')
        plt.figure()
        pyemma.plots.plot_implied_timescales(its,units='ns',dt=0.25)
        plt.savefig('{0}_its_{1}.jpg'.format(project_name,i),dpi=300)
        plt.close()

def estimate_n_macrostates(msm,metastability_threshold=400):
    return sum(msm.timescales()>metastability_threshold)

def plot_free_energies(cg_model):
    f_i = -np.log(sorted(cg_model.stationary_distribution))[::-1]
    f_i -= f_i.min()
    plt.figure()
    plt.plot(f_i,'.')
    plt.xlabel('Macrostate')
    plt.ylabel(r'$\Delta G$ $(k_B T)$')
    plt.title('Macrostate free energies')
    plt.savefig('{0}_macrostate_free_energies.jpg'.format(project_name),dpi=300)
    plt.close()

# def parse_filename(filename):
#     ''' Return RUN trajectory '''
#     import re
#     #filenamename = 'blah-blah-/no-solvent/run0-clone0.h5'
#     index = len(filename) - filename[::-1].find('-clone'[::-1]) - 8
#     run_string = re.findall('\/run\d.',filename)[-1]
#     run = int(run_string[4:-1])
#     return run

# def load_dataset(filenames):
#     trajs = [md.load(f) for f in filenames]
#
# def build_index(filenames):
#     ''' associate each filename with the length of the trajectory'''

# if __name__=='__main__':
#     '''
#     inputs:
#         dtrajs
#     '''
    ## time between snapshots:
    #from simtk import unit as u
    #time_per_frame=250*u.picosecond

    #dt = time_per_frame.value_in_unit(u.nanosecond)


    # disc = pyemma.coordinates.discretizer(source,transform=tica,cluster=kmeans)

    ## all this is obviated by the above few lines
    # for i,f in enumerate(filenames):
    #     print('{0}/{1}'.format(i,len(filenames)))
    #     traj = md.load(f)
    #     distances,_ = md.compute_contacts(traj,contacts=respairs_that_changed,scheme=scheme)
    #
    #     X.append(distances)
    #
    # from msmbuilder.featurizer import DihedralFeaturizer
    # dih_model = DihedralFeaturizer()
    # X_dih = dih_model.fit_transform(trajs)
    #
    # feature_sets = [X,X_dih]
    # X_combined = [np.hstack([x[i] for x in feature_sets]) for i in range(len(feature_sets[0]))]
    #
    # # tICA
    # import pyemma
    # tica = pyemma.coordinates.tica(X_combined,lag=50,kinetic_map=True)
    # Y = tica.get_output()
    # print("Dimensionality after tICA, retaining enough eigenvectors to explain 0.95 of kinetic variation: {0}".format(np.vstack(Y).shape[1]))
    #
    # inds = np.argmax(tica.feature_TIC_correlation,axis=1)
    # corrs = np.abs(tica.feature_TIC_correlation[inds,0])
    #
    # plt.plot(np.cumsum(tica_combined.eigenvalues))
    #
    # if Y[0].shape[1] > max_tics:
    #     Y = [y[:,:max_tics] for y in Y]
    #
    # # discretize
    # k_means = pyemma.coordinates.cluster_mini_batch_kmeans(Y_,k=500,max_iter=1000)
    # #uniform_time_clustering = pyemma.coordinates.cluster_uniform_time(Y,k=100)
    # dtrajs = [np.array(dtraj)[:,0] for dtraj in k_means.get_output()]
