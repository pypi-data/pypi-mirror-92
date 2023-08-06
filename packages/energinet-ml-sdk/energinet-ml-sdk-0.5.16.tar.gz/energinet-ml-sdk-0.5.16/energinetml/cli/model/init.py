import os
import click
import click_spinner

from energinetml.backend import default_backend as backend
from energinetml.settings import (
    DEFAULT_VM_CPU,
    DEFAULT_VM_GPU,
    COMMAND_NAME,
)
from energinetml.core.model import (
    Model,
    DEFAULT_FILES_INCLUDE,
    DEFAULT_FILES_EXCLUDE,
)

from .utils import discover_project


# Constants  TODO Move to Project class?
MODEL_FILES = ('__init__.py', 'model.json', 'model.py')


# -- Input parsing and validation --------------------------------------------


def _parse_input_model_name(ctx, param, value):
    """
    TODO
    """
    if value is None:
        value = click.prompt(
            text='Please enter a model name',
            type=str,
        )
    return value


# -- CLI Command -------------------------------------------------------------


@click.command()
@discover_project()
@click.option('--name', '-n',
              required=False, default=None, type=str,
              callback=_parse_input_model_name,
              help='Model name (must be unique in project)')
def init_model(name, project):
    """
    Create a new, empty machine learning model.
    \f

    TODO Verify name complies to naming conventions
    TODO Length of ComputeTarget name must be <= 16

    :param str name:
    :param Project project:
    """

    # -- Target folder -------------------------------------------------------

    path = project.default_model_path(name)

    # Confirm overwrite files if they exists
    for filename in MODEL_FILES:
        if os.path.isfile(os.path.join(path, filename)):
            click.echo('File already exists: %s'
                       % os.path.join(path, filename))
            if not click.confirm('Really override existing %s?' % filename):
                raise click.Abort()

    # Create empty folder is necessary
    if not os.path.isdir(path):
        os.makedirs(path)

    # -- Create model --------------------------------------------------------

    model = Model.create(
        path=path,
        name=name,
        experiment=name,
        compute_target=None,
        vm_size=None,
        files_include=DEFAULT_FILES_INCLUDE,
        files_exclude=DEFAULT_FILES_EXCLUDE,
    )

    click.echo('-' * 79)
    click.echo('Initialized the model at: %s' % path)
    click.echo('')
    click.echo((
        'Next step is to implement your model script! I have created an '
        'empty model template for you. It is called %s and is located in '
        'the model directory. Also, remember to add your model\'s '
        'dependencies to requirements.txt (located at the root '
        'of your project).'
    ) % Model.SCRIPT_FILE_NAME)
    click.echo('')
    click.echo('Use "%s model ..." to interact with your model afterwards.'
               % COMMAND_NAME)
    click.echo('-' * 79)

    # -- Compute cluster -----------------------------------------------------

    cluster, vm_size = _setup_compute_cluster(project, backend.get_workspace(
        subscription_id=project.subscription_id,
        resource_group=project.resource_group,
        name=project.workspace_name,
    ))

    model.compute_target = cluster
    model.vm_size = vm_size
    model.save()


# -- Helper functions --------------------------------------------------------


def _setup_compute_cluster(project, workspace):
    """
    TODO
    """
    new_or_existing_cluster = click.prompt(
        text='Would you like to setup a new compute cluster, or use an existing one?',
        type=click.Choice(['new', 'existing']),
    )

    if new_or_existing_cluster == 'new':
        return _create_new_compute_cluster(project, workspace)
    elif new_or_existing_cluster == 'existing':
        return _use_existing_compute_cluster(workspace)


def _create_new_compute_cluster(project, workspace):
    """
    TODO
    """
    available_vm_sizes = backend.get_available_vm_sizes(workspace)
    available_vm_size_mapped = {vm['name']: vm for vm in available_vm_sizes}

    click.echo((
        'You can either specific an exact VM Size, or use a default '
        'VM Size for either CPU or GPU computation.'
    ))
    vm_size_or_gpu_or_cpu = click.prompt(
        text='How would you like to specify VM Size?',
        type=click.Choice(['vmsize', 'cpu', 'gpu']),
    )

    vm_size = None
    cluster = None

    if vm_size_or_gpu_or_cpu == 'vmsize':
        vm_size = click.prompt(
            text='Please enter a VM size',
            type=click.Choice(available_vm_size_mapped),
        )
    elif vm_size_or_gpu_or_cpu == 'cpu':
        vm_size = DEFAULT_VM_CPU
        cluster = 'CPU-Cluster'
    elif vm_size_or_gpu_or_cpu == 'gpu':
        vm_size = DEFAULT_VM_GPU
        cluster = 'GPU-Cluster'

    if vm_size not in available_vm_size_mapped:
        click.echo('VM Size unavailable: %s' % vm_size)
        vm_size = click.prompt(
            text='Please enter a VM size',
            type=click.Choice(available_vm_size_mapped),
        )

    if cluster is None:
        cluster = vm_size.replace('_', '-')

    min_nodes = click.prompt(
        text='Please enter minimum nodes available',
        default=0,
        type=int,
    )

    max_nodes = click.prompt(
        text='Please enter maximum nodes available',
        default=1,
        type=int,
    )

    cluster = click.prompt(
        text='Please enter a name for the compute cluster',
        default=cluster,
        type=str,
    )

    existing_clusters = backend.get_compute_clusters(workspace)
    existing_cluster_names = [c.name for c in existing_clusters]

    while cluster in existing_cluster_names:
        click.echo('Cluster already exists: %s' % cluster)
        cluster = click.prompt(
            text='Please enter a name for the compute cluster',
            default=cluster,
            type=str,
        )

    click.echo('Creating compute cluster "%s" using VM Size: %s'
               % (cluster, vm_size))

    with click_spinner.spinner():
        backend.create_compute_cluster(
            workspace=workspace,
            name=cluster,
            vm_size=vm_size,
            min_nodes=min_nodes,
            max_nodes=max_nodes,
            vnet_resource_group_name=project.resource_group,
            vnet_name=project.vnet_name,
            subnet_name=project.subnet_name,
        )

    return cluster, vm_size


def _use_existing_compute_cluster(workspace):
    """
    TODO
    """
    existing_clusters = backend.get_compute_clusters(workspace)
    existing_clusters_mapped = {c.name: c for c in existing_clusters}
    existing_cluster_names = [c.name for c in existing_clusters]

    if len(existing_clusters) == 0:
        click.echo('No compute clusters exists in workspace "%s"'
                   % workspace.name)
        raise click.Abort()

    default = existing_cluster_names[0] \
        if len(existing_cluster_names) == 1 \
        else None

    cluster = click.prompt(
        text='Please enter name of existing compute cluster',
        type=click.Choice(existing_cluster_names),
        default=default,
    )

    return cluster, existing_clusters_mapped[cluster].vm_size
