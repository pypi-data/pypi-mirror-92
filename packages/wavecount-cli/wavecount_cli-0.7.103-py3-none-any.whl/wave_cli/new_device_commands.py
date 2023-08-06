import click
import PyInquirer as inq
from click.termui import style
from examples import custom_style_1

from wave_cli.utils import save_config
from wave_cli.services.backend_services import Backend
from wave_cli.services.validate_services import IntValidate, StringValidate, SerialNumberValidate


@click.command(name='new', help='Register a new device.')
@click.pass_context
def new(ctx):
    try:
        company_choices = ['new']
        backend_service = Backend(context=ctx)
        result = backend_service.sync_cache()
        customers = result
        ctx.obj['customers'] = customers
        company_choices.extend(customers)
        answer = inq.prompt(
            questions=[
                {
                    'type': 'input',
                    'name': 'serial_number',
                    'message': 'Enter device "serial-number"',
                    'validate': SerialNumberValidate,
                }
            ],
            style=custom_style_1
        )
        serial_number: str = answer['serial_number']
        answer = inq.prompt(
            questions=[
                {
                    'type': 'list',
                    'name': 'company',
                    'message': 'Select "company"',
                    'choices': company_choices,
                    'validate': StringValidate,
                }
            ],
            style=custom_style_1
        )
        company: str = answer['company']
        if company == 'new':
            answers = inq.prompt(
                style=custom_style_1,
                questions=[
                    {
                        'type': 'input',
                        'name': 'company',
                        'message': 'Enter "company"',
                        'validate': StringValidate,
                    },
                    {
                        'type': 'input',
                        'name': 'store',
                        'message': 'Enter "store"',
                        'validate': StringValidate,
                    },
                    {
                        'type': 'input',
                        'name': 'store_number',
                        'message': 'Enter "store number"',
                        'validate': IntValidate,
                    },
                ],
            )
            company: str = answers['company']
            customers[company] = {}
            store: str = answers['store']
            store_number: str = answers['store_number']
            customers[company][store] = store_number
            save_config(ctx.obj)
        else:
            store_choices = ['new']
            store_choices.extend(sorted(customers[company].keys()))
            answer = inq.prompt(
                style=custom_style_1,
                questions=[
                    {
                        'type': 'list',
                        'name': 'store',
                        'message': 'Enter "store"',
                        'choices': store_choices,
                        'validate': StringValidate,
                    },
                ],
            )
            store: str = answer['store']
            if store == 'new':
                answer = inq.prompt(
                    style=custom_style_1,
                    questions=[
                        {
                            'type': 'input',
                            'name': 'store',
                            'message': 'Enter "store"',
                            'validate': StringValidate,
                        },
                        {
                            'type': 'input',
                            'name': 'store_number',
                            'message': 'Enter "store number"',
                            'validate': IntValidate,
                        },
                    ],
                )
                customers[company] = {}
                store: str = answer['store']
                store_number: str = answer['store_number']
                customers[company][store] = store_number
                save_config(ctx.obj)
            else:
                store_number: str = customers[company][store]
        data = {
            'store': store,
            'company': company,
            'storeNumber': store_number,
            'serialNumber': serial_number,
        }
        device = backend_service.register_device(data)
        dev_id = device['deviceId']
        prim_key = device['symmetricKey']['primaryKey']
        comp = device['company']
        store = device['store']
        store_num = device['storeNumber']
        sn = device['serialNumber']
        click.secho(' Seria lNumber:  {}'.format(sn), fg='green')
        click.secho(' Device Id:      {}'.format(dev_id), fg='green')
        click.secho(' Primary Key:    {}'.format(prim_key), fg='green')
        click.secho(' Company:        {}'.format(comp), fg='green')
        click.secho(' Store:          {}'.format(store), fg='green')
        click.secho(' Store Number:   {}'.format(store_num), fg='green')
        click.secho()
    except Exception as e:
        exit()
